import logging
import sys
import time

from .config import config
from .db import Database
from .scan import initial_scan, periodic_scan
from .mc import get_online_player_number

logging.basicConfig(
    level=config["logging_level"],
    format="%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def main():
    if not Database.exists():
        initial_scan()

    command = sys.argv[1] if len(sys.argv) > 1 else ""

    if command == "scan":
        modified_files, sha_changed_files = periodic_scan()
        logging.info(f"Number of modified files: {len(modified_files)}")
        logging.info(f"Number of files with changed xxh32: {len(sha_changed_files)}")

    elif command == "monitor":
        while True:
            if config["minecraft_server"]["enabled"] and get_online_player_number() > 0:
                modified_files, sha_changed_files = periodic_scan()
                logging.info(f"Number of modified files: {len(modified_files)}")
                logging.info(
                    f"Number of files with changed xxh32: {len(sha_changed_files)}"
                )

                time.sleep(config["monitor"]["interval"])


if __name__ == "__main__":
    main()
