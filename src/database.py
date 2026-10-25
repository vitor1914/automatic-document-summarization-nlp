import sqlite3
from contextlib import contextmanager
from typing import Iterator

from src.config import DATABASE_FILE, SCHEMA_FILE, create_directories


def initialize_database() -> None:
    """Create database tables and indexes."""
    create_directories()

    with sqlite3.connect(DATABASE_FILE) as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        schema = SCHEMA_FILE.read_text(encoding="utf-8")
        connection.executescript(schema)


@contextmanager
def get_connection() -> Iterator[sqlite3.Connection]:
    """Provide a database connection with foreign keys enabled."""
    create_directories()
    connection = sqlite3.connect(DATABASE_FILE)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")

    try:
        yield connection
    finally:
        connection.close()