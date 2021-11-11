from datetime import date
import subprocess
import json
from pathlib import Path

conf = Path('./conf')
today = date.today()

with open(conf/'settings.json', 'r') as s:
    settings = json.load(s)
log_dir = Path(settings['log_dir'])
b = settings['backups']
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
        excludes = str(Path(conf/entry['excludes']).absolute())
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