#!/bin/sh
export PATH=$PATH:/usr/local/bin
 
# Change Directory
cd /home/opc
 

# Run Program
python ./trade_bot/amonitoring.py I >> /home/opc/logs/amonitoring.log 2>&1
