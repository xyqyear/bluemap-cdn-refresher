import logging
import os

from .config import config
from .db import connect_db, get_file, insert_file, update_file
from .utils import compute_xxh32


def initial_scan():
    conn, cursor = connect_db()
    count = 0

    with conn:
        for folder in config["monitor"]["folders"]:
            for root, dirs, files in os.walk(folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    modify_date = int(os.path.getmtime(file_path))
                    xxh32 = compute_xxh32(file_path)
                    insert_file(cursor, file_path, modify_date, xxh32)
                    count += 1
                logging.info("Inserted %d files into database", count)
        conn.commit()


def periodic_scan():
    conn, cursor = connect_db()
    modified_files = []
    sha_changed_files = []

    with conn:
        for folder in config["monitor"]["folders"]:
            for root, dirs, files in os.walk(folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    modify_date = int(os.path.getmtime(file_path))
                    row = get_file(cursor, file_path)
                    if row:
                        if modify_date > row[0]:
                            modified_files.append(file_path)
                            xxh32 = compute_xxh32(file_path)
                            if xxh32 != row[1]:
                                logging.debug("xxh32 changed for %s", file_path)
                                update_file(cursor, file_path, modify_date, xxh32)
                                sha_changed_files.append(file_path)
                    else:
                        xxh32 = compute_xxh32(file_path)
                        insert_file(cursor, file_path, modify_date, xxh32)
        conn.commit()

    return modified_files, sha_changed_files
