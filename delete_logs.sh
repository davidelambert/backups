#!/bin/bash

cd $1
RETAIN_DATE=$2

for FILE in * ; do
    if [[ ${FILE%.log} < $RETAIN_DATE ]] ; then
        rm -f $FILE
    fi
done