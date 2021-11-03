from datetime import date
import json
from pathlib import Path

today = date.today()
conf = Path('./conf')
log_dir = Path('./backup_logs')

with open(conf/'settings.json', 'r') as s:
    settings = json.load(s)

b = settings['backups']
for name, data in b.items():
    print('\nName: ', name)
    print('Data: ', data)

# =============================================


test = b['test']

if 'excludes' in test.keys() and test['excludes'] is not None:
    excludes = str(Path(conf/test['excludes']).absolute())
else:
    excludes = ''

if 'log' in test.keys() and test['log'] is True:
    log = str(log_dir.absolute()) + '/test_' + str(today) + '.log'
else:
    log = ''


with open('./output/test', 'w') as f:

    f.write(f"""#!/bin/bash\n
SOURCE={test['source']}
DEST={test['dest']}
EXCLUDES={excludes}
LOG={log}
rsync -az --exclude-from=$EXCLUDES --log-file=$LOG $SOURCE $DEST 
""")