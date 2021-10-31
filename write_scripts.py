from datetime import date, timedelta
import json
from pathlib import Path

today = date.today()
conf = Path('./conf')

with open(conf/'settings.json', 'r') as s:
    settings = json.load(s)

b = settings['backups']
for name, data in b.items():
    print('\nName: ', name)
    print('Data: ', data)

test = b['hotrod_home']
with open('./output/test', 'w') as f:
    f.write('#!/bin/bash\n\n')
    f.writelines([
        'SOURCE={}'.format(test['source']),
        'DEST={}'.format(test['dest']),
        ''
    ])