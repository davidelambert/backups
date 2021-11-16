from pathlib import Path
import subprocess
import json
from datetime import date, timedelta

conf_dir = Path('./conf')
log_dir = Path('./backup_logs')

with open(conf_dir/'config.json', 'r') as c:
    config = json.load(c)


def backup(entry:dict):
    """Takes an entry from the parsed JSON settings
    (settings['backups']), processes the entry's values,
    and passes processed values as arguments to a system-executed
    rsync command via subprocess.call().
    """

    # last word of source path, excluding trailing slashes
    src_name = entry['source'].strip('/').split('/')[-1]

    
    #TODO: more input validation

    if 'excludes' in entry.keys() and entry['excludes'] is not None:
        excludes = str(Path(conf_dir/entry['excludes']).absolute())
    else:
        excludes = ''

    if 'log' in entry.keys() and entry['log'] is True:
        log = f'{log_dir.absolute()}/{src_name}_{date.today()}.log'
    else:
        log = ''

    # TODO: file size limit
    subprocess.call(['rsync', '-abCz', '--delete-before',
                    '--backup-dir=archive_`date +%F`',
                    '--exclude=archive_*',
                    f'--exclude-from={excludes}',
                    f'--log-file={log}',
                    entry['source'],
                    entry['dest']])


def cleanup(entry:dict):
    """Deletes the destination archive directory (containing
    previous versions of files synced by backup()) dated _int_
    days ago, where _int_ is read from the config.json entry's
    'retain_days' key, if present."""

    #TODO: input validation
    

    cleanup_date = date.today() - timedelta(days=entry['retain_days'])
    dest_server = entry['dest'].split(':')[0]
    dest_path = entry['dest'].split(':')[-1]


    #TODO: log rm output
    src_name = entry['source'].strip('/').split('/')[-1]
    log = f'{log_dir.absolute()}/{src_name}_{date.today()}.log'


    subprocess.call(['ssh', dest_server, 'rm', '-rfv',
                     f'{dest_path}archive_{cleanup_date}/'])


test = config['test']
backup(test)
cleanup(test)




# for name, data in b.items():
#     print('\nName: ', name)
#     print('Data: ', data)