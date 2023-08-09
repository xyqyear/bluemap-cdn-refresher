import hashlib
import json
from .file import get_data


def compute_sha256(file_path):
    if file_path.endswith(".json.gz"):
        json_data = get_data(file_path)
        return hashlib.sha256(json.dumps(json_data).encode()).hexdigest()
    else:
        h = hashlib.sha256()
        with open(file_path, "rb") as file:
            while chunk := file.read(4096):
                h.update(chunk)
        return h.hexdigest()
