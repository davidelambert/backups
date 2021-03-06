#!/bin/bash

# ==============================================================
# Back up (most of) home directory to a spare laptop on the LAN.
# 
# Sample anacrontab entry
# @daily    30  home-backup.daily   /full/path/to/script
# ==============================================================

PROJECT_ROOT=$HOME/projects/backups

SOURCE=$HOME/
SERVER=clunker.lan
REMOTE_DIR=$HOME/hotrod-backup
DEST=$REMOTE_DIR/current


TODAY=$(date -I)
YESTERDAY=$(date -I -d "1 day ago")

RETAIN_DAYS=14
RETAIN_DATE=$(date -I -d "$RETAIN_DAYS days ago")
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

# create log & backup directories if they don't exist
[[ ! -d "$LOG_DIR" ]] && mkdir -p $LOG_DIR
ssh $SERVER "[[ ! -d '$REMOTE_DIR' ]] && mkdir -p $REMOTE_DIR"

# delete logs & backups older than retention period
$PROJECT_ROOT/delete_logs.sh "$LOG_DIR" "$RETAIN_DATE"
ssh $SERVER "bash -s" < $PROJECT_ROOT/delete_backups.sh "$REMOTE_DIR" "$RETAIN_DATE"

# execture the sync as a background job
rsync $ARGS $SOURCE $SERVER:$DEST & job=$!

# display a spinner while rsync job is running
printf "Working...  "
while kill -0 $job 2>/dev/null ; do
    for s in / - \\ \|; do
        printf "\b$s"
        sleep .1
    done
done
printf "\b  \n"
