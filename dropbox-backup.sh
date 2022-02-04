#!/bin/bash

# ===================================================
# Back up (most of) the Dropbox directory via rsync
# Sample crontab entry, running daily at 4:00am:
# 0 4 * * * /full/path/to/script/dropbox-backup.sh
# ===================================================

# NOTE: TO BE RUN LOCALLY ON CLUNKER

SOURCE=$HOME/Dropbox
DEST=/media/delamb/backup

TODAY=$(date "+%F")
LOG_DIR=$HOME/.log/dropbox-backup
DELETE_OFFSET=$(date "+%F" -d "30 days ago")

EXCLUDE_PATTERNS=(".dropbox.cache/" ".dropbox")
EXCLUDES=""
for pattern in ${EXCLUDE_PATTERNS[@]}; do
    EXCLUDES+=" --exclude=${pattern}"
done

ARGS="-Chaz"
KWARGS="--delete --delete-excluded --force"

# create log directory if it doesn"t exist
if [ ! -d "$LOG_DIR" ] ; then
    mkdir -p $LOG_DIR
fi

# delete logs older than delete offset
if [ -f "$LOG_DIR/$DELETE_OFFSET.log" ] ; then
    rm -f "$LOG_DIR/$DELETE_OFFSET.log"
fi

# do it
rsync $ARGS $KWARGS $EXCLUDES --log-file=$LOG_DIR/$TODAY.log $SOURCE $DEST

