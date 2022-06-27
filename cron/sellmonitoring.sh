#!/bin/sh
export PATH=$PATH:/usr/local/bin
 
# Change Directory
cd /home/opc
 

# Run Program
python ./trade_bot/test2.py I >> /home/opc/logs/sellmonitoring.log 2>&1
