import hashlib


def compute_sha256(file_path):
    h = hashlib.sha256()
    with open(file_path, "rb") as file:
        while chunk := file.read(4096):
            h.update(chunk)
    return h.hexdigest()
