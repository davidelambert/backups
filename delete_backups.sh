#!/bin/bash

cd $1
RETAIN_DATE=$2

for DIR in .*/ ; do
    if [[ ${DIR:0:8} == ".backup_" ]] ; then
        if [[ ${DIR#.backup_} < $RETAIN_DATE ]] ; then
            rm -rf $DIR
        fi
    fi
done
