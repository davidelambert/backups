from datetime import date, timedelta
import subprocess
import json
from pathlib import Path

today = date.today()
# TODO: timedeltas

remote_id = 'delamb@clunker.lan'
conf = Path('./conf')

with open(conf/'backups_config.json', 'r') as f:
    b = json.load(f)
    # TODO: nest directory list in a level so other settings can be added?

for i in range(len(b)):
    # TODO: control flow for period
    dest_this = f'{b[i]["dest"]}_{today.strftime("%Y-%m-%d")}'

    remote_full = f'{remote_id}:{dest_this}'
    excludes = f'--exclude-from={str(conf.absolute())}/{b[i]["excludes"]}'

    subprocess.call(["ssh", remote_id, "mkdir", dest_this])

    subprocess.call(["rsync", "-avz", "-e", "ssh",
                     excludes, b[i]["source"], remote_full])
