import sqlite3
from .config import config


def connect_db():
    conn = sqlite3.connect(config["database_file"])
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS files (
            path TEXT PRIMARY KEY,
            modify_date INTEGER,
            xxh32 INTEGER
        )
    """
    )
    conn.commit()
    return conn, cursor


def insert_file(cursor, path, modify_date, xxh32):
    cursor.execute("INSERT INTO files VALUES (?, ?, ?)", (path, modify_date, xxh32))


def update_file(cursor, path, modify_date, xxh32):
    cursor.execute(
        "UPDATE files SET modify_date = ?, xxh32 = ? WHERE path = ?",
        (modify_date, xxh32, path),
    )


def get_file(cursor, path):
    cursor.execute("SELECT modify_date, xxh32 FROM files WHERE path = ?", (path,))
    return cursor.fetchone()
