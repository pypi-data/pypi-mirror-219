"""Database built into Reflex."""

from collections import defaultdict
from pathlib import Path
from typing import Any, Optional

import sqlalchemy
import sqlmodel

from reflex.base import Base
from reflex.config import get_config

from . import constants

try:
    import alembic.autogenerate  # pyright: ignore [reportMissingImports]
    import alembic.command  # pyright: ignore [reportMissingImports]
    import alembic.operations.ops  # pyright: ignore [reportMissingImports]
    import alembic.runtime.environment  # pyright: ignore [reportMissingImports]
    import alembic.script  # pyright: ignore [reportMissingImports]
    import alembic.util  # pyright: ignore [reportMissingImports]
    from alembic.config import Config  # pyright: ignore [reportMissingImports]

    has_alembic = True
except ImportError:
    has_alembic = False


def get_engine(url: Optional[str] = None):
    """Get the database engine.

    Args:
        url: the DB url to use.

    Returns:
        The database engine.

    Raises:
        ValueError: If the database url is None.
    """
    conf = get_config()
    url = url or conf.db_url
    if url is None:
        raise ValueError("No database url configured")
    return sqlmodel.create_engine(
        url,
        echo=False,
        connect_args={"check_same_thread": False} if conf.admin_dash else {},
    )


class Model(Base, sqlmodel.SQLModel):
    """Base class to define a table in the database."""

    # The primary key for the table.
    id: Optional[int] = sqlmodel.Field(primary_key=True)

    def __init_subclass__(cls):
        """Drop the default primary key field if any primary key field is defined."""
        non_default_primary_key_fields = [
            field_name
            for field_name, field in cls.__fields__.items()
            if field_name != "id" and getattr(field.field_info, "primary_key", None)
        ]
        if non_default_primary_key_fields:
            cls.__fields__.pop("id", None)

        super().__init_subclass__()

    def dict(self, **kwargs):
        """Convert the object to a dictionary.

        Args:
            kwargs: Ignored but needed for compatibility.

        Returns:
            The object as a dictionary.
        """
        return {name: getattr(self, name) for name in self.__fields__}

    @staticmethod
    def create_all():
        """Create all the tables."""
        engine = get_engine()
        sqlmodel.SQLModel.metadata.create_all(engine)

    @staticmethod
    def get_db_engine():
        """Get the database engine.

        Returns:
            The database engine.
        """
        return get_engine()

    @staticmethod
    def _alembic_config():
        """Get the alembic configuration and script_directory.

        Returns:
            tuple of (config, script_directory)
        """
        config = Config(constants.ALEMBIC_CONFIG)
        return config, alembic.script.ScriptDirectory(
            config.get_main_option("script_location", default="version"),
        )

    @staticmethod
    def _alembic_render_item(
        type_: str,
        obj: Any,
        autogen_context: "alembic.autogenerate.api.AutogenContext",
    ):
        """Alembic render_item hook call.

        This method is called to provide python code for the given obj,
        but currently it is only used to add `sqlmodel` to the import list
        when generating migration scripts.

        See https://alembic.sqlalchemy.org/en/latest/api/runtime.html

        Args:
            type_: one of "schema", "table", "column", "index",
                "unique_constraint", or "foreign_key_constraint"
            obj: the object being rendered
            autogen_context: shared AutogenContext passed to each render_item call

        Returns:
            False - indicating that the default rendering should be used.
        """
        autogen_context.imports.add("import sqlmodel")
        return False

    @classmethod
    def _alembic_autogenerate(cls, connection: sqlalchemy.engine.Connection) -> bool:
        """Generate migration scripts for alembic-detectable changes.

        Args:
            connection: sqlalchemy connection to use when detecting changes

        Returns:
            True when changes have been detected.
        """
        config, script_directory = cls._alembic_config()
        revision_context = alembic.autogenerate.api.RevisionContext(
            config=config,
            script_directory=script_directory,
            command_args=defaultdict(
                lambda: None,
                autogenerate=True,
                head="head",
            ),
        )
        writer = alembic.autogenerate.rewriter.Rewriter()

        @writer.rewrites(alembic.operations.ops.AddColumnOp)
        def render_add_column_with_server_default(context, revision, op):
            # Carry the sqlmodel default as server_default so that newly added
            # columns get the desired default value in existing rows
            if op.column.default is not None and op.column.server_default is None:
                op.column.server_default = sqlalchemy.DefaultClause(
                    sqlalchemy.sql.expression.literal(op.column.default.arg),
                )
            return op

        def run_autogenerate(rev, context):
            revision_context.run_autogenerate(rev, context)
            return []

        with alembic.runtime.environment.EnvironmentContext(
            config=config,
            script=script_directory,
            fn=run_autogenerate,
        ) as env:
            env.configure(
                connection=connection,
                target_metadata=sqlmodel.SQLModel.metadata,
                render_item=cls._alembic_render_item,
                process_revision_directives=writer,  # type: ignore
            )
            env.run_migrations()
        changes_detected = False
        if revision_context.generated_revisions:
            upgrade_ops = revision_context.generated_revisions[-1].upgrade_ops
            if upgrade_ops is not None:
                changes_detected = bool(upgrade_ops.ops)
        if changes_detected:
            for _script in revision_context.generate_scripts():
                pass  # must iterate to actually generate the scripts
        return changes_detected

    @classmethod
    def _alembic_upgrade(
        cls,
        connection: sqlalchemy.engine.Connection,
        to_rev: str = "head",
    ) -> None:
        """Apply alembic migrations up to the given revision.

        Args:
            connection: sqlalchemy connection to use when performing upgrade
            to_rev: revision to migrate towards
        """
        config, script_directory = cls._alembic_config()

        def run_upgrade(rev, context):
            return script_directory._upgrade_revs(to_rev, rev)

        # apply updates to database
        with alembic.runtime.environment.EnvironmentContext(
            config=config,
            script=script_directory,
            fn=run_upgrade,
        ) as env:
            env.configure(connection=connection)
            env.run_migrations()

    @classmethod
    def automigrate(cls) -> Optional[bool]:
        """Generate and execute migrations for all sqlmodel Model classes.

        If alembic is not installed or has not been initialized for the project,
        then no action is performed.

        If models in the app have changed in incompatible ways that alembic
        cannot automatically generate revisions for, the app may not be able to
        start up until migration scripts have been corrected by hand.

        Returns:
            True - indicating the process was successful
            None - indicating the process was skipped
        """
        if not has_alembic or not Path(constants.ALEMBIC_CONFIG).exists():
            return

        with cls.get_db_engine().connect() as connection:
            cls._alembic_upgrade(connection=connection)
            changes_detected = cls._alembic_autogenerate(connection=connection)
            if changes_detected:
                cls._alembic_upgrade(connection=connection)
            connection.commit()
        return True

    @classmethod
    @property
    def select(cls):
        """Select rows from the table.

        Returns:
            The select statement.
        """
        return sqlmodel.select(cls)


def session(url: Optional[str] = None) -> sqlmodel.Session:
    """Get a session to interact with the database.

    Args:
        url: The database url.

    Returns:
        A database session.
    """
    return sqlmodel.Session(get_engine(url))
