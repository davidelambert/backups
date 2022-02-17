#!/bin/bash

# ======================================================
# Back up (most of) home directory to a spare laptop
# on the LAN. Ignore Dropbox, VMs, & version ctl files.
#
# Sample anacrontab entry
# @daily    30  home-backup.daily   /full/path/to/script
# ======================================================

SOURCE=$HOME/
SERVER=clunker.lan
REMOTE_DIR=$HOME/hotrod-backup
DEST=$REMOTE_DIR/current


TODAY=$(date "+%F")
YESTERDAY=$(date "+%F" -d "1 day ago")

RETAIN_DAYS=14
RETAIN_DATE=$(date "+%F" -d "$RETAIN_DAYS days ago")
RETAIN_DIR=$REMOTE_DIR/.backup_$YESTERDAY
RETAIN_DELETE=$REMOTE_DIR/.backup_$RETAIN_DATE

EXCLUDES=$HOME/backup_excludes

LOG_DIR=$HOME/.log/home-backup

ARGS="-hhaz --stats
      --delete --delete-excluded
      --force --ignore-errors 
      --exclude-from=$EXCLUDES
      --backup --backup-dir=$RETAIN_DIR
      --log-file=$LOG_DIR/$TODAY.log"

# create log directory if it doesn't exist
if [ ! -d "$LOG_DIR" ] ; then
    mkdir -p $LOG_DIR
fi

# delete log after retention period
if [ -f "$LOG_DIR/$RETAIN_DATE.log" ] ; then
    rm -f "$LOG_DIR/$RETAIN_DATE.log"
fi

# delete backup dir after retention period
ssh $SERVER "[[ -d '$RETAIN_DELETE' ]] && rm -rf $RETAIN_DELETE"

# abbreviated command
echo 'Working...'
rsync $ARGS $SOURCE $SERVER:$DEST
echo 'Done.'
