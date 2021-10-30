from datetime import date
import subprocess
import json

today = date.today()

remote_id = "delamb@clunker.lan"
remote_base = "hotrod_backup"
excludes_base = "/home/delamb/Dropbox/projects/backups/excludes"

with open("./backups_config.json", "r") as f:
    b = json.load(f)

for i in range(len(b)):
    dest_today = f'{remote_base}/{b[i]["dest"]}_{today.strftime("%Y-%m-%d")}'
    excludes = f'--exclude-from={excludes_base}/{b[i]["excludes"]}'
    remote_full = f'{remote_id}:{dest_today}'

    subprocess.call(["ssh", remote_id, "mkdir", dest_today])

    subprocess.call(["rsync", "-avz", "-e", "ssh", "--del",
                     excludes, b[i]["source"], remote_full])
