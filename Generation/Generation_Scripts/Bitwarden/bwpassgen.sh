#!/bin/bash

# upper (u), lower (l), number (n), special (s)
# length iterations filename configuration (all/l/ls/ld/sd)

LENGTH=$1
END=$2
FILENAME=$3
CONFIG=$4

if [ "$CONFIG" == "all" ]
then
    for i in $(seq 1 $END); do ./bw generate -ulns --length $LENGTH >> $FILENAME; done
fi

if [ "$CONFIG" == "l" ]
then
    for i in $(seq 1 $END); do ./bw generate -ul --length $LENGTH >> $FILENAME; done
fi

if [ "$CONFIG" == "ls" ]
then
    for i in $(seq 1 $END); do ./bw generate -uls --length $LENGTH >> $FILENAME; done
fi

if [ "$CONFIG" == "ld" ]
then
    for i in $(seq 1 $END); do ./bw generate -uln --length $LENGTH >> $FILENAME; done
fi

if [ "$CONFIG" == "sd" ]
then
    for i in $(seq 1 $END); do ./bw generate -ns --length $LENGTH >> $FILENAME; done
fi