#!/bin/sh
export PATH=$PATH:/usr/local/bin
 
# Change Directory
cd /home/opc
 

# Run Program
python ./trade_bot/DCA_BTC.py I >> /home/opc/logs/monitoring.log 2>&1
