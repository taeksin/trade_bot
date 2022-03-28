#!/bin/bash

while [ 1 ]
do
    pid=`ps -ef | grep "amonitoring" | grep -v 'grep' | awk '{print $2}'`

    if [ -z $pid ]
    then
        echo $PATH
        ./amonitoring.py&
    fi
    sleep 5
done