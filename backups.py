from datetime import date
import subprocess

today = date.today()

remote_id = "delamb@clunker.lan"
remote_base = "hotrod_backup"
excludes_base = "/home/delamb/Dropbox/projects/backups/excludes"

b = [
    {"source": "/home/delamb/",
     "excludes": "excludes-home",
     "dest": "home"},

    {"source": "/home/delamb/.config/",
     "excludes": "excludes-.config",
     "dest": ".config"},

    {"source": "/home/delamb/.local",
     "excludes": "excludes-.local",
     "dest": ".local"}
]

for i in range(len(b)):
    dest_today = f'{remote_base}/{b[i]["dest"]}_{today.strftime("%Y-%m-%d")}'
    excludes = f'--exclude-from={excludes_base}/{b[i]["excludes"]}'
    remote_full = f'{remote_id}:{dest_today}'

    subprocess.call(["ssh", remote_id, "mkdir", dest_today])

    subprocess.call(["rsync", "-avz", "-e", "ssh", "--del",
                     excludes, b[i]["source"], remote_full])
