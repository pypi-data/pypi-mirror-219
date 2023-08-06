from pathlib import Path
from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlite3 import Connection as SQLite3Connection
from sqlmodel import SQLModel, create_engine

from . import models  # noqa
from .version import __version__  # noqa


def create_sqlite_engine(path, echo: bool = False):
    engine = create_engine(f"sqlite:///{Path(path).absolute()}", echo=echo)

    # Create tables:
    SQLModel.metadata.create_all(engine)

    @event.listens_for(Engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        if isinstance(dbapi_connection, SQLite3Connection):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

    return engine
