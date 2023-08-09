import sys
import time
from .config import config
from .db import connect_db
from .scan import initial_scan, periodic_scan


def main():
    conn, cursor = connect_db()

    cursor.execute("SELECT COUNT(*) FROM files")
    if cursor.fetchone()[0] == 0:
        initial_scan()

    command = sys.argv[1] if len(sys.argv) > 1 else ""

    if command == "scan":
        modified_files, sha_changed_files = periodic_scan()
        print(f"Number of modified files: {len(modified_files)}")
        print(f"Number of files with changed SHA256: {len(sha_changed_files)}")
        return

    if command == "monitor":
        while True:
            modified_files, sha_changed_files = periodic_scan()
            print(f"Number of modified files: {len(modified_files)}")
            print(f"Number of files with changed SHA256: {len(sha_changed_files)}")

            with open(config["file_list"], "w") as file:
                for path in sha_changed_files:
                    file.write(path + "\n")

            time.sleep(config["monitor"]["interval"])


if __name__ == "__main__":
    main()