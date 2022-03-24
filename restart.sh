#!/bin/bash

while [ 1 ]
do
    pid=`ps -ef | grep "amonitoring" | grep -v 'grep' | awk '{print $2}'`

    if [ -z $pid ]
    then
        echo "amonitoring start"
        sudo /trade_bot/nohup python3 amonitoring.py > output.log &
    fi
    sleep 5
done