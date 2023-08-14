import plyvel
from .config import config

import os
import struct


class Database:
    def __init__(self, path=config["database_path"]):
        self.db = plyvel.DB(path, create_if_missing=True)
        self.wb = None

    @staticmethod
    def exists(path=config["database_path"]):
        return os.path.exists(path)

    @staticmethod
    def pack_fileinfo(modify_date, xxh32):
        return struct.pack("<II", modify_date, xxh32)

    @staticmethod
    def unpack_fileinfo(data):
        return struct.unpack("<II", data)

    def initiate_transaction(self):
        if self.wb is not None:
            raise Exception("Already in transaction")
        self.wb = self.db.write_batch(transaction=True)

    def commit_transaction(self, close=True):
        if self.wb is None:
            raise Exception("Not in transaction")
        self.wb.write()
        if close:
            self.wb = None

    def insert_fileinfo(self, path, modify_date, xxh32):
        if self.wb is None:
            raise Exception("Not in transaction")
        self.wb.put(path.encode(), self.pack_fileinfo(modify_date, xxh32))

    def update_fileinfo(self, path, modify_date, xxh32):
        self.insert_fileinfo(path, modify_date, xxh32)

    def get_fileinfo(self, path):
        return self.unpack_fileinfo(self.db.get(path.encode()))
