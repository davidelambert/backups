#! python3

from datetime import date
import subprocess

remote_id = "delamb@clunker.lan"
remote_base = "hotrod_backup"
excludes_base = "/home/delamb/.config/backup-scripts"

bu = [
    {"source": "/home/delamb/",
     "excludes": "excludes-dotfiles",
     "dest": "dotfiles_" + date.today().isoformat()}
]

for i in range(len(bu)):
    dest_today = f'{remote_base}/{bu[i]["dest"]}'
    excludes = f'--exclude-from={excludes_base}/{bu[i]["excludes"]}'
    remote_full = f'{remote_id}:{dest_today}'

    subprocess.call(["ssh", remote_id, "mkdir", dest_today])

    subprocess.call(["rsync", "-avz", "-e", "ssh", "--del",
                     excludes, bu[i]["source"], remote_full])
