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
            sha256 TEXT
        )
    """
    )
    conn.commit()
    return conn, cursor


def insert_file(path, modify_date, sha256):
    conn, cursor = connect_db()
    cursor.execute("INSERT INTO files VALUES (?, ?, ?)", (path, modify_date, sha256))
    conn.commit()


def update_file(path, modify_date, sha256):
    conn, cursor = connect_db()
    cursor.execute(
        "UPDATE files SET modify_date = ?, sha256 = ? WHERE path = ?",
        (modify_date, sha256, path),
    )
    conn.commit()


def get_file(path):
    conn, cursor = connect_db()
    cursor.execute("SELECT modify_date, sha256 FROM files WHERE path = ?", (path,))
    return cursor.fetchone()
