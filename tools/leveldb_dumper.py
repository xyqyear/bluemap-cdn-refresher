from bluemap_cdn_refresher.db import Database
import datetime

# dump the database
db = Database()

for key, value in db.db:
    modify_dat, xxh32 = db.unpack_fileinfo(value)
    datestring = datetime.datetime.fromtimestamp(modify_dat).strftime("%Y-%m-%d %H:%M:%S")
    print(f"date: {datestring}, xxh32: {xxh32}, path: {key.decode()}")
