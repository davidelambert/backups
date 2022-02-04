#!/bin/bash

# ======================================================
# Back up (most of) home directory to a spare laptop
# on the LAN. Ignore Dropbox, VMs, & version ctl files.
#
# Sample crontab entry, running daily at 2:00am:
# 0 2 * * * /full/path/to/script/home-backup.sh
# ======================================================

SOURCE=$HOME/rig/
SERVER=clunker.lan
DEST=$HOME/hotrod-backup

TODAY=$(date "+%F")
YESTERDAY=$(date "+%F" -d "1 day ago")
YESTERWEEK=$(date "+%F" -d "1 week ago")
YESTERMONTH=$(date "+%F" -d "1 month ago")

RETAIN_DIR=".backup_$YESTERDAY"
RETAIN_DELETE=".backup_$YESTERWEEK"

LOG_DIR=$HOME/.log/home-backup

EXCLUDE_PATTERNS=("Dropbox/" "VirtualBox*/")
EXCLUDES=""
for pattern in ${EXCLUDE_PATTERNS[@]}; do
    EXCLUDES+=" --exclude=${pattern}"
done

ARGS="-Chaz"
KWARGS="--delete --delete-excluded --force --ignore-errors $EXCLUDES
        --backup --backup-dir=$DEST/$RETAIN_DIR --log-file=$LOG_DIR/$TODAY.log"

# create log directory if it doesn't exist
if [ ! -d "$LOG_DIR" ] ; then
    mkdir -p $LOG_DIR
fi

# delete log from a month ago
if [ -f "$LOG_DIR/$YESTERMONTH.log" ] ; then
    rm -f "$LOG_DIR/$YESTERMONTH.log"
fi

# delete backup dir from a week ago
ssh $SERVER [[ -d "$DEST/$RETAIN_DELETE" ]] && rm -rf $DEST/$RETAIN_DELETE

# abbreviated command
rsync $ARGS $KWARGS $SOURCE $SERVER:$DEST