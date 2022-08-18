#!/bin/bash

# ==============================================================
# Back up (most of) home directory to a spare laptop on the LAN.
# 
# Sample anacrontab entry
# @daily    30  home-backup.daily   /full/path/to/script
# ==============================================================

SERVER=hotrod.lan
SRC=~
DST=~/backup
EXCLUDES=./backup_excludes

ARGS="-hhazi --backup
      --backup-dir=$HOME/backup/archive
      --delete --delete-excluded
      --exclude-from=$EXCLUDES
      --log-file=./test.log"

rsync $ARGS $SERVER:$SRC $DEST & job=$!

printf "Working...  "
while kill -0 $job 2>/dev/null ; do
    for s in / - \\ \|; do
        printf "\b$s"
        sleep .1
    done
done
printf "\b  \n"

