from datetime import date
import subprocess
import json
from pathlib import Path


conf = Path('./conf')
with open(conf/'settings.json', 'r') as s:
    settings = json.load(s)

today = date.today()
log_dir = Path(settings['log_dir'])

b = settings['backups']
test = b['test']



if 'excludes' in test.keys() and test['excludes'] is not None:
    excludes = str(Path(conf/test['excludes']).absolute())
else:
    excludes = ''

if 'log' in test.keys() and test['log'] is True:
    log = str(log_dir.absolute()) + '/test_' + str(today) + '.log'
else:
    log = ''


subprocess.call(['rsync', '-az',
                 f'--exclude-from={excludes}',
                 f'--log-file={log}',
                 test['source'], test['dest']])


# for name, data in b.items():
#     print('\nName: ', name)
#     print('Data: ', data)