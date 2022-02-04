#!/bin/bash

# ======================================================
# Back up (most of) home directory to a spare laptop
# on the LAN. Ignore Dropbox, VMs, & version ctl files.
#
# Sample crontab entry, running daily at 2:00am:
# 0 2 * * * /full/path/to/script/home-backup.sh
# ======================================================

SOURCE=$HOME/
SERVER=clunker.lan
REMOTE_DIR=$HOME/hotrod-backup
DEST=$REMOTE_DIR/current


TODAY=$(date "+%F")
YESTERDAY=$(date "+%F" -d "1 day ago")
YESTERWEEK=$(date "+%F" -d "1 week ago")
YESTERMONTH=$(date "+%F" -d "1 month ago")

RETAIN_DIR=$REMOTE_DIR/.backup_$YESTERDAY
RETAIN_DELETE=$REMOTE_DIR/.backup_$YESTERWEEK

EXCLUDES=$HOME/backup_excludes

LOG_DIR=$HOME/.log/home-backup

ARGS="--dry-run -hhaz --stats
      --delete --delete-excluded
      --force --ignore-errors 
      --exclude-from=$EXCLUDES
      --backup --backup-dir=$RETAIN_DIR
      --log-file=$LOG_DIR/$TODAY.log"

# create log directory if it doesn't exist
if [ ! -d "$LOG_DIR" ] ; then
    mkdir -p $LOG_DIR
fi

# delete log from 1 month ago
if [ -f "$LOG_DIR/$YESTERMONTH.log" ] ; then
    rm -f "$LOG_DIR/$YESTERMONTH.log"
fi

# delete backup dir from 1 week ago
ssh $SERVER "[[ -d '$RETAIN_DELETE' ]] && rm -rf $RETAIN_DELETE"

# abbreviated command
rsync $ARGS $SOURCE $SERVER:$DEST