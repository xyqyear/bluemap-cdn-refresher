import gzip
import json


def get_data(file_path):
    with gzip.open(file_path, "rb") as f:
        return json.load(f)["tileGeometry"]["data"]
