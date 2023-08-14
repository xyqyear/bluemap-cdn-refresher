import logging
import os

from .config import config
from .db import Database
from .utils import compute_xxh32


def initial_scan():
    db = Database()
    count = 0

    db.initiate_transaction()
    for folder in config["monitor"]["folders"]:
        for root, dirs, files in os.walk(folder):
            for file in files:
                if file.endswith(".filepart"):
                    continue

                file_path = os.path.join(root, file)
                modify_date = int(os.path.getmtime(file_path))
                xxh32 = compute_xxh32(file_path)
                db.insert_fileinfo(file_path, modify_date, xxh32)

                count += 1
                if count % 1000 == 0:
                    db.commit_transaction(close=False)

            logging.info("Inserted %d files into database", count)
    db.commit_transaction()


def periodic_scan():
    db = Database()
    modified_files = []
    sha_changed_files = []

    db.initiate_transaction()
    for folder in config["monitor"]["folders"]:
        for root, dirs, files in os.walk(folder):
            for file in files:
                if file.endswith(".filepart"):
                    continue
                file_path = os.path.join(root, file)
                modify_date = int(os.path.getmtime(file_path))
                fileinfo = db.get_fileinfo(file_path)
                if fileinfo:
                    if modify_date > fileinfo[0]:
                        modified_files.append(file_path)
                        xxh32 = compute_xxh32(file_path)
                        if xxh32 != fileinfo[1]:
                            logging.debug("xxh32 changed for %s", file_path)
                            db.update_fileinfo(file_path, modify_date, xxh32)
                            sha_changed_files.append(file_path)
                else:
                    xxh32 = compute_xxh32(file_path)
                    db.insert_fileinfo(file_path, modify_date, xxh32)
        db.commit_transaction(close=False)
    db.commit_transaction()

    return modified_files, sha_changed_files
