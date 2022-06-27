#!/bin/bash
 
timestamp=`date +%Y/%m/%d/%H:%M`
 
# BUY PROCESS CHECK
PID=`ps -ef |grep -w 'trade_bot/test2.py' |grep -v grep|awk '{print $2}'`
 
if [ -z "$PID" ]
then
        echo "$timestamp"
        echo 'MONITORING PROCESS DEAD'
        /home/opc/cron/sellmonitoring.sh
else
        echo "$timestamp"
        echo 'sellMONITORING PROCESS IS RUNNING'
fi