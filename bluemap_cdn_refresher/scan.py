import os
from datetime import datetime
from .utils import compute_sha256
from .db import update_file, get_file, insert_file
from .config import config


def initial_scan():
    for folder in config["monitor"]["folders"]:
        for root, dirs, files in os.walk(folder):
            for file in files:
                file_path = os.path.join(root, file)
                modify_date = int(os.path.getmtime(file_path))
                sha256 = compute_sha256(file_path)
                insert_file(file_path, modify_date, sha256)


def periodic_scan():
    modified_files = []
    sha_changed_files = []
    for folder in config["monitor"]["folders"]:
        for root, dirs, files in os.walk(folder):
            for file in files:
                file_path = os.path.join(root, file)
                modify_date = int(os.path.getmtime(file_path))
                row = get_file(file_path)
                if row:
                    if modify_date > row[0]:
                        modified_files.append(file_path)
                        sha256 = compute_sha256(file_path)
                        if sha256 != row[1]:
                            update_file(file_path, modify_date, sha256)
                            sha_changed_files.append(file_path)
                else:
                    sha256 = compute_sha256(file_path)
                    insert_file(file_path, modify_date, sha256)
    return modified_files, sha_changed_files
