from pathlib import Path
import os
import shutil
import subprocess
import json
from datetime import date

conf_dir = Path('./conf')
today = date.today()

with open(conf_dir/'config.json', 'r') as s:
    config = json.load(s)
log_dir = Path(config['log_dir'])
b = config['backups']
test = b['test']

def backup(entry:dict, title:str):
    """Takes an entry from the parsed JSON settings
    (settings['backups']), processes the entry's values,
    and passes processed values as arguments to a system-executed
    rsync command via subprocess.call().
    """

    source = entry['source']
    dest = entry['dest'] + '/' + title + '_' + str(today)

    if 'excludes' in entry.keys() and entry['excludes'] is not None:
        excludes = str(Path(conf_dir/entry['excludes']).absolute())
    else:
        excludes = ''

    if 'log' in entry.keys() and entry['log'] is True:
        log = str(log_dir.absolute()) + '/' + title + '_' + str(today) + '.log'
    else:
        log = ''

    subprocess.call(['rsync', '-az',
                    f'--exclude-from={excludes}',
                    f'--log-file={log}',
                    source, dest])


backup(test, '.jupyter')


# for name, data in b.items():
#     print('\nName: ', name)
#     print('Data: ', data)