import hashlib
import json
import time
import logging

from .file import get_data


def compute_sha256(file_path):
    if file_path.endswith(".json.gz"):
        before = time.perf_counter()
        json_data = get_data(file_path)
        then = time.perf_counter()
        logging.debug(f"read data: {then - before}")
        sha256 = hashlib.sha256(json.dumps(json_data).encode()).hexdigest()
        logging.debug(f"sha256: {time.perf_counter() - then}")
        return sha256
    else:
        h = hashlib.sha256()
        with open(file_path, "rb") as file:
            while chunk := file.read(4096):
                h.update(chunk)
        return h.hexdigest()
