#!/bin/sh
export PATH=$PATH:/usr/local/bin
 
# Change Directory
cd /home/opc
 

# Run Program
python ./trade_bot/test1.py I >> /home/opc/logs/buymonitoring.log 2>&1
