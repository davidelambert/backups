#!/bin/bash

# ===================================================
# Back up local Zotero database to Dropbox via rsync
# Sample crontab entry, running daily at 2:00am:
# 0 2 * * * /full/path/to/script/zotero-backup.sh
# ===================================================

SOURCE=$HOME/Zotero/
DEST=$HOME/Dropbox/articles/Zotero

TODAY=$(date '+%F')
LOG_DIR=$HOME/.log/zotero-backup
DELETE_OFFSET=$(date "+%F" -d "30 days ago")

# omit -C option: no version control files to ignore
ARGS="-haz"
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

