#!/bin/sh
export PATH=$PATH:/usr/local/bin
 
# Change Directory
cd /home/opc/venv/myvenv/bin/trade_bot/
 

# Run Program
nohup python3 DCA_BTC.py > output.log &

