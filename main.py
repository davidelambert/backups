from pathlib import Path
import subprocess
import json
from datetime import date, timedelta

conf_dir = Path('./conf')
log_dir = Path('./backup_logs')

with open(conf_dir/'config.json', 'r') as c:
    config = json.load(c)


def backup(entry:dict):
    """Takes an entry from config.json and passes processed
    entry values as arguments to an rsync subprocess.
    """

    # last word of source path, excluding trailing slashes
    src_name = entry['src'].strip('/').split('/')[-1]

    
    #TODO: more input validation

    if 'dest_server' in entry.keys() and entry['dest_server'] is not None:
        if 'dest_user' in entry.keys() and entry['dest_user'] is not None:
            user = f"{entry['dest_user']}@"
        else:
            user = ''
        remote = f"{user}{entry['dest_server']}:"
    else:
        remote = ''

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
                    entry['src'],
                    f"{remote}{entry['dest_path']}"])


def cleanup(entry:dict):
    """Deletes the destination archive directory (containing
    previous versions of files synced by backup()) dated {int}
    days ago. {int} is read from the config.json entry's
    'retain_days' key, if present, and defaults to 7 otherwise.
    """

    # target archive directory to delete
    if 'retain_days' in entry.keys() and entry['retain_days'] is not None:
        cleanup_date = date.today() - timedelta(days=entry['retain_days'])
    else:
        cleanup_date = date.today() - timedelta(days=7)
    cleanup_target = f"{entry['dest_path']}archive_{cleanup_date}/"

    # user/server if destination is remote
    if 'dest_server' in entry.keys() and entry['dest_server'] is not None:
        if 'dest_user' in entry.keys() and entry['dest_user'] is not None:
            user = f"{entry['dest_user']}@"
        else:
            user = ''
        remote = f"{user}{entry['dest_server']}"
    else:
        remote = ''

    # delete remote/local target directory
    if remote != '':
        subprocess.call(['ssh', remote, 'rm', '-rfv', cleanup_target])
    else:
        subprocess.call(['rm', '-rfv', cleanup_target])


    #TODO: log rm output
    # src_name = entry['src'].strip('/').split('/')[-1]
    # log = f'{log_dir.absolute()}/{src_name}_{date.today()}.log'


test = config['test']
backup(test)
cleanup(test)




# for name, data in b.items():
#     print('\nName: ', name)
#     print('Data: ', data)