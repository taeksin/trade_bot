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
#ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
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
#ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ


# 자동매매 시작
#print("autotrade start")
# 프로그램 시작 메세지 발송
message = '\n\n[📀📀 시작 안내 📀📀]'
message = message + '\n\n DCA_BTC 시작! '
message = message + '\n\n- 현재시간:' + str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))

# 프로그램 시작 메세지 발송
upbit.send_telegram_message(message)

# 알림 발송 용 변수
sent_list = []

while True:
    try:
        # 시간ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
        now = datetime.now()                                 # 현재시간
        start_time = get_start_time("KRW-BTC")               # 시작시간      9:00
        buy_time = start_time + timedelta(hours=16)          # 구매시간      01:00
        end_time = buy_time + timedelta(minutes=5)  # 종료시간      01:05
        
        # 시간ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
        #ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
        # 주문 + 메시지ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
        available_amt = upbit.get_krwbal()['available_krw']
        if int(available_amt)>5050:
            # 01:00 < now < 01:05
            now = datetime.now()
            print(f' buy={buy_time}\n now={now}\n end={end_time}')
            upbit.send_telegram_message("1번째 if까지는 okay")
            if buy_time>now:
                upbit.send_telegram_message("buy가now보다 크다")
            else:
                upbit.send_telegram_message("buy가now보다 작다")
            if buy_time < now < end_time:
                message = '- buy:' + str(buy_time)
                message = message + '\n- now:' + str(now)
                message = message + '\n- end:' + str(end_time)
                upbit.send_telegram_message(message)
                rtn_buycoin_mp = upbit.buycoin_mp("KRW-BTC", 5000)
                upbit.send_telegram_message("🔴🟥BTC 구매 완료🟥🔴"+"\n - 현재가 "+ str(get_current_price("KRW-BTC")))
                time.sleep(240)
                buy_time=buy_time+timedelta(days=1)
                end_time=end_time+timedelta(days=1)
                '''
                # 알림 Key 조립
                msg_key = {'TYPE': 'PCNT-UP','ITEM': "KRW-BTC"}

                # 메세지 조립
                message = '\n\n[🔴🟥구매완료 안내!🟥🔴]'
                message = message + '\n\n- 종목: ' + "KRW-BTC"
                message = message + '\n- 현재가: ' + str(get_current_price("KRW-BTC"))
                    
                # 메세지 발송(1시간:3600초 간격)
                sent_list = upbit.send_msg(sent_list, msg_key, message, '3600')
                '''
        else :
            message = '\n\n  🔋🔌 ༼ つ ◕_◕ ༽つ 🔌🔋\n 🔋 총알이 떨어졌습니다. \n 🔋 장전해주세요'
            message = message + '\n\n- 현재시간:' + str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
            # 프로그램 종료 메세지 발송
            sent_list = upbit.send_msg(sent_list, 0, message, '3600')
        # 주문 + 메시지ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ


    except KeyboardInterrupt:
        # 프로그램 종료 메세지 조립
        message = '\n\n[🚨❌🚨종료🚨❌🚨]'
        message = message + '\n\n DCA_BTC 종료!'
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
        message = message + '\n\n DCA_BTC 종료!'
        message = message + '\n\n- 현재시간:' + str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
        # 프로그램 종료 메세지 발송
        upbit.send_telegram_message(message)
        
        logging.error("Exception 발생!")
        logging.error(traceback.format_exc())
        sys.exit(-200)
