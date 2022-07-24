#!/bin/sh
export PATH=$PATH:/usr/local/bin
 
# Change Directory
cd /home/opc/
 
# Run Program
nohup python3 ./trade_bot/DCA.py I >> /home/opc/cron/logs/DCA1.log 2>&1
