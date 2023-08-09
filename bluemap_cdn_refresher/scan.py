import logging
import os

from .config import config
from .db import connect_db, get_file, insert_file, update_file
from .utils import compute_sha256


def initial_scan():
    conn, cursor = connect_db()

    with conn:
        for folder in config["monitor"]["folders"]:
            for root, dirs, files in os.walk(folder):
                for file in files:
                    logging.debug("Scanning %s", file)
                    file_path = os.path.join(root, file)
                    modify_date = int(os.path.getmtime(file_path))
                    sha256 = compute_sha256(file_path)
                    insert_file(cursor, file_path, modify_date, sha256)
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
                            sha256 = compute_sha256(file_path)
                            if sha256 != row[1]:
                                logging.debug("SHA256 changed for %s", file_path)
                                update_file(cursor, file_path, modify_date, sha256)
                                sha_changed_files.append(file_path)
                    else:
                        sha256 = compute_sha256(file_path)
                        insert_file(cursor, file_path, modify_date, sha256)
        conn.commit()

    return modified_files, sha_changed_files
