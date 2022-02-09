import os
import sys
import logging
import math
import traceback
import logging
import requests
import time
import smtplib
import jwt
import sys
import uuid
import hashlib
import math
import numpy
import pandas as pd
from datetime import datetime, timedelta
from decimal import Decimal
from urllib.parse import urlencode
from module import upbit
# 공통 모듈 Import
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from module import upbit as upbit  # noqa
 
# -----------------------------------------------------------------------------
# - Name : main
# - Desc : 메인
# -----------------------------------------------------------------------------
if __name__ == '__main__':
 
    # noinspection PyBroadException
    try:
 
        print("***** USAGE ******")
        print("[1] 로그레벨(D:DEBUG, E:ERROR, 그외:INFO)")
 
        # 로그레벨(D:DEBUG, E:ERROR, 그외:INFO)
        upbit.set_loglevel('I')
 
        # ---------------------------------------------------------------------
        # Logic Start!
        # ---------------------------------------------------------------------
        # 보유 종목 리스트 조회
        #candle_data = upbit.get_candle('KRW-AXS', 'D', '1')
        #df = pd.DataFrame(candle_data)
        #logging.info("change_rate : "+str(float(df['change_rate']*100)))
        
        
        target_items = upbit.get_items('KRW', '')
        for target_item in target_items:
            a=upbit.get_change_rate(target_item['market'])
            logging.info(target_item['market']+"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!a="+str(a))
            
            '''
            candle_data = upbit.get_candle(target_item['market'], 'D', '1')
            df = pd.DataFrame(candle_data)
            name=str(target_item['market'])
            #logging.info(str(target_item['market'])+"    change_rate : "+str(float(df['change_rate']*100)))
            logging.info('%-10s'%str(target_item['market'])+" change_rate : "+str('%.4f'%float(df['change_rate']*100)))
          '''
 
        a=upbit.get_change_rate('KRW-AXS')
        logging.info("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!a="+str(a))
 
 
 
    except KeyboardInterrupt:
        logging.error("KeyboardInterrupt Exception 발생!")
        logging.error(traceback.format_exc())
        sys.exit(1)
 
    except Exception:
        logging.error("Exception 발생!")
        logging.error(traceback.format_exc())
        sys.exit(1)