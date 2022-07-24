import time
import pyupbit
import datetime
import os
import sys
import logging
import traceback
from decimal import Decimal
from datetime import timedelta
from datetime import datetime
# 공통 모듈 Import
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from module import upbit
#ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)  # 업비트에서  ohclv를 일봉으로 조회하면 시작 시간이 나옴
    start_time = df.index[0]
    return start_time

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]
#ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ

# 자동매매 시작
#print("autotrade start")
# 프로그램 시작 메세지 발송
message = '\n\n[📀📀 시작 안내 📀📀]'
message = message + '\n\n DCA 시작! '
message = message + '\n\n- 현재시간:' + str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))

# 프로그램 시작 메세지 발송
upbit.send_telegram_message(message)

# 알림 발송 용 변수
sent_list = []

while True:
    try:
        #ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
        # 주문 + 메시지ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
        available_amt = upbit.get_krwbal()['available_krw']
        if int(available_amt)>15075:
            # 시간ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
            now = datetime.now()                                 # 현재시간
            start_time = get_start_time("KRW-BTC")               # 시작시간      9:00
            buy_time = start_time + timedelta(hours=16)          # 구매시간      01:00
            end_time = buy_time + timedelta(minutes=3)           # 종료시간      01:03
            # 시간ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
            
            #print(f' buy={buy_time}\n now={now}\n end={end_time}')
            #print(f' buy={buy_time.timestamp()}\n now={now.timestamp()}\n end={end_time.timestamp()}')
            
            # 01:00 < now < 01:03
            #서버에는 if buy_time.timestamp() < now.timestamp()<end_time.timestamp() :
            if buy_time.timestamp() < now.timestamp()<end_time.timestamp() :
                rtn_buycoin_mp = upbit.buycoin_mp("KRW-BTC", 10000)
                message ='- 현재시간:' + str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                upbit.send_telegram_message("🔴🟥BTC 구매 완료🟥🔴"+"\n - 현재가 "+ str(get_current_price("KRW-BTC"))+"\n" + message)
                rtn_buycoin_mp = upbit.buycoin_mp("KRW-ETH", 5000)
                message ='- 현재시간:' + str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                upbit.send_telegram_message("🔴🟥BTC 구매 완료🟥🔴"+"\n - 현재가 "+ str(get_current_price("KRW-ETH"))+"\n" + message)
                time.sleep(86000)
            else:
                #print("시간 조건이 안맞는다")
                time.sleep(0.3)
        else :
            message = '\n\n  🔋🔌 ༼ つ ◕_◕ ༽つ 🔌🔋\n 🔋 총알이 떨어졌습니다. \n 🔋 장전해주세요'
            message = message + '\n\n- 현재시간:' + str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
            # 프로그램 종료 메세지 발송
            sent_list = upbit.send_msg(sent_list, 0, message, '3600')
        # 주문 + 메시지ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ


    except KeyboardInterrupt:
        # 프로그램 종료 메세지 조립
        message = '\n\n[🚨❌🚨종료🚨❌🚨]'
        message = message + '\n\n DCA 종료!'
        message = message + '\n\n KeyboardInterrupt Exception 발생!'
        message = message + '\n\n- 현재시간:' + str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
        
        # 프로그램 종료 메세지 발송
        upbit.send_telegram_message(message)
        logging.error("KeyboardInterrupt Exception 발생!")
        logging.error(traceback.format_exc())
        sys.exit(-100)

    except Exception:
        # 프로그램 종료 메세지 조립
        message = '\n\n[🚨❌🚨종료🚨❌🚨]'
        message = message + '\n\n DCA 종료!'
        message = message + '\n\n Exception 발생!'
        message = message + '\n\n- 현재시간:' + str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
        
        # 프로그램 종료 메세지 발송
        upbit.send_telegram_message(message)
        logging.error("Exception 발생!")
        logging.error(traceback.format_exc())
        sys.exit(-200)
