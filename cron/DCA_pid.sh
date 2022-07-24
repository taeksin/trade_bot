#!/bin/bash
 
timestamp=`date +%Y/%m/%d/%H:%M`
 
# BUY PROCESS CHECK
PID=`ps -ef |grep -w 'trade_bot/DCA.py' |grep -v grep|awk '{print $2}'`
 
if [ -z "$PID" ]
then
        echo "$timestamp"
        echo 'DCA PROCESS DEAD'
        /home/opc/cron/DCA.sh
else
        echo "$timestamp"
        echo 'DCA PROCESS IS RUNNING'
fi