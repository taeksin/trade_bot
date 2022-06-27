#!/bin/bash
 
timestamp=`date +%Y/%m/%d/%H:%M`
 
# BUY PROCESS CHECK
PID=`ps -ef |grep -w 'trade_bot/DCA_BTC.py' |grep -v grep|awk '{print $2}'`
 
if [ -z "$PID" ]
then
        echo "$timestamp"
        echo 'MONITORING PROCESS DEAD'
        /home/opc/cron/monitoring.sh
else
        echo "$timestamp"
        echo 'MONITORING PROCESS IS RUNNING'
fi