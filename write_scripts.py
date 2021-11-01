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
source = test['source']
dest = test['dest']
excludes = str(Path(conf/test['excludes']).absolute())
cmd = 'rsync -avz --exclude-from={0} {1} {2}'.format(excludes, source, dest)


# TODO: write this shit a multiline string

with open('./output/test', 'w') as f:
    if test['log'] is not None:
        f.writelines([
            '#!/bin/bash\n\n',
            'TODAY=$(date \'+%F\')\n',
            'LOG_DIR={}\n'.format(test['log']['dir']),
            'LOG_PREFIX={}\n'.format(test['log']['prefix']),
            'THIS_LOG=$LOG_DIR/$(echo $LOG_PREFIX)_$TODAY.log\n',
            'LOG_DELETE_OFFSET=$(date \'+%F\' -d \'{} ago\')\n\n'.format(test['log']['delete_offset']),
            '# create backup directory if it doesn\'t exist\n',
            'if [ ! -d "$LOG_DIR" ] ; then\n',
            '    mkdir $LOG_DIR\n',
            'fi\n\n',
            '# print datetime header to log\n',
            'printf "RSYNC LOG $(date \'+%F %H:%M:%S\')\\n$(printf \'=%.0s\' ={1..39})\\n" >> $THIS_LOG\n\n',
            '# rsync and log verbose output\n',
            cmd + ' >> $THIS_LOG\n\n',
            '# 2 blank lines, in case of multiple backups in a day\n',
            'printf "\\n\\n" >> $THIS_LOG\n\n',
            '# clean up old logs\n',
            'if [ -f "$LOG_DIR/$(echo $LOG_PREFIX)_$LOG_DELETE_OFFSET.log" ] ; then\n',
            '    rm $LOG_DIR/$(echo $LOG_PREFIX)_$LOG_DELETE_OFFSET.log\n',
            'fi\n',
            ''
        ])
    else:
        f.writelines(['#!/bin/bash\n\n', cmd, '\n'])