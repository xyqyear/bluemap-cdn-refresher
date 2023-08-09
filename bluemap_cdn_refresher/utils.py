import xxhash
import gzip


def compute_xxh32(file_path):
    if file_path.endswith(".json.gz"):
        with gzip.open(file_path, "rb") as f:
            raw_json = f.read()
        key_string = raw_json[88:92]
        if key_string != b'data':
            raise ValueError(f"the data format changed for bluemap")
        xxh32 = xxhash.xxh32(raw_json[93:]).intdigest()
        return xxh32
    else:
        file_content = open(file_path, "rb").read()
        return xxhash.xxh32(file_content).intdigest()
