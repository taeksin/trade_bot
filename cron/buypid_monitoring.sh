#!/bin/bash
 
timestamp=`date +%Y/%m/%d/%H:%M`
 
# BUY PROCESS CHECK
PID=`ps -ef |grep -w 'trade_bot/test1.py' |grep -v grep|awk '{print $2}'`
 
if [ -z "$PID" ]
then
        echo "$timestamp"
        echo 'MONITORING PROCESS DEAD'
        /home/opc/cron/buymonitoring.sh
else
        echo "$timestamp"
        echo 'buyMONITORING PROCESS IS RUNNING'
fi