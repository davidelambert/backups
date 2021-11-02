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
    if test['log'] is not None:
        f.write(f"""#!/bin/bash

SOURCE={test['source']}
DEST={test['dest']}
EXCLUDES={str(Path(conf/test['excludes']).absolute())}

TODAY=$(date '+%F')
LOG_DIR={test['log']['dir']}
LOG_PREFIX={test['log']['prefix']}
THIS_LOG=$LOG_DIR/$(echo $LOG_PREFIX)_$TODAY.log
LOG_DELETE_OFFSET=$(date '+%F' -d '{test['log']['delete_offset']} ago')

# create backup directory if it doesn't exist
if [ ! -d "$LOG_DIR" ] ; then
    mkdir $LOG_DIR
fi

# print datetime header to log
printf "RSYNC LOG $(date '+%F %H:%M:%S')\\n" >> $THIS_LOG

# rsync and log verbose output
rsync -avz --exclude-from=$EXCLUDES $SOURCE $DEST >> $THIS_LOG

# 2 blank lines, in case of multiple backups in a day
printf "\\n\\n" >> $THIS_LOG

# clean up old logs
if [ -f "$LOG_DIR/$(echo $LOG_PREFIX)_$LOG_DELETE_OFFSET.log" ] ; then
    rm $LOG_DIR/$(echo $LOG_PREFIX)_$LOG_DELETE_OFFSET.log
fi
""")
    else:
        f.write(f"""#!/bin/bash

SOURCE={test['source']}
DEST={test['dest']}
EXCLUDES={str(Path(conf/test['excludes']).absolute())}

rsync -az --exclude-from=$EXCLUDES $SOURCE $DEST
""")