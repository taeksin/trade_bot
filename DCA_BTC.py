import time
import os
import sys
import logging
import traceback
import pyupbit
from datetime import datetime
from datetime import timedelta
from decimal import Decimal

# 공통 모듈 Import
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from module import upbit

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


# -----------------------------------------------------------------------------
# - Name : start_buytrade
# - Desc : 매수 로직
# - Input
# 1) buy_amt : 매수금액
# -----------------------------------------------------------------------------
def start_buytrade(buy_amt):
    try:
        # 프로그램 시작 메세지 발송
        message = '\n\n[💲💲 시작 안내 💲💲]'
        message = message + '\n\n DCA_BTC 시작! '
        message = message + '\n\n- 현재시간:' + str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))

        # 프로그램 시작 메세지 발송
        upbit.send_telegram_message(message)

        # ---------------------------------------------------------------------
        # 알림 발송 용 변수
        # ---------------------------------------------------------------------
        sent_list = []
        # ---------------------------------------------------------------------
        # -----------------------------------------------------------------
        # 전체 종목 리스트 추출
        # -----------------------------------------------------------------
        target_items = upbit.get_items('KRW', '')
        # ----------------------------------------------------------------------
        # 반복 수행
        # ----------------------------------------------------------------------
        while True:
            now =datetime.now()                            # 현재시간
            start_time = get_start_time("KRW-BTC")         # 시작시간      9:00
            end_time = start_time + timedelta(days=1)      # 종료시간
            buy_time = start_time - timedelta(hours=8)     # 구매시간      01:00
            
            if buy_time<now<buy_time+timedelta(minutes=5):
                print("hi")
            

            # -----------------------------------------------------------------
            # 종목별 체크
            # -----------------------------------------------------------------
            for target_item in target_items:
                    # ------------------------------------------------------------------
                    # 매수금액 설정
                    # 1. M : 수수료를 제외한 최대 가능 KRW 금액만큼 매수
                    # 2. 금액 : 입력한 금액만큼 매수
                    # ------------------------------------------------------------------
                    available_amt = upbit.get_krwbal()['available_krw']

                    if buy_amt == '5000':
                        buy_amt = available_amt

                    # ------------------------------------------------------------------
                    # 입력 금액이 주문 가능금액보다 작으면 종료
                    # ------------------------------------------------------------------
                    if Decimal(str(available_amt)) < Decimal(str(buy_amt)):
                        logging.info('주문 가능금액[' + str(available_amt) + ']이 입력한 주문금액[' + str(buy_amt) + '] 보다 작습니다.')
                        continue

                    # ------------------------------------------------------------------
                    # 최소 주문 금액(업비트 기준 5000원) 이상일 때만 매수로직 수행
                    # ------------------------------------------------------------------
                    if Decimal(str(buy_amt)) < Decimal(str(upbit.min_order_amt)):
                        logging.info('주문금액[' + str(buy_amt) + ']이 최소 주문금액[' + str(upbit.min_order_amt) + '] 보다 작습니다.')
                        continue

                    # ------------------------------------------------------------------
                    # 시장가 매수
                    # 실제 매매를 원하시면 테스트를 충분히 거친 후 주석을 해제하시면 됩니다.
                    # ------------------------------------------------------------------
                    logging.info('시장가 매수 시작! [' + str(target_item['market']) + ']')
                    rtn_buycoin_mp = upbit.buycoin_mp("KRW-BTC", buy_amt)
                    upbit.send_telegram_message("💲💲"+"BTC 구매 완료💲💲")
                    upbit.send_telegram_message('\n- 현재가: ' + str(get_current_price("KRW-BTC")))
                    logging.info('시장가 매수 종료! [' + str(target_item['market']) + ']')
                    logging.info(rtn_buycoin_mp)
                    '''
                    # 알림 Key 조립
                    msg_key = {'TYPE': 'PCNT-UP','ITEM': target_item['market']}

                    # 메세지 조립
                    message = '\n\n[🔴🟥구매완료 안내!🟥🔴]'
                    message = message + '\n\n- 종목: ' + str(target_item['market'])
                    message = message + '\n- 현재가: ' + str(target_item['trade_price'])
                    
                    # 메세지 발송(1시간:3600초 간격)
                    sent_list = upbit.send_msg(sent_list, msg_key, message, '3600')
                    '''
                    
    # ---------------------------------------
    # 모든 함수의 공통 부분(Exception 처리)
    # ----------------------------------------
    except Exception:
        raise


# -----------------------------------------------------------------------------
# - Name : main
# - Desc : 메인
# -----------------------------------------------------------------------------
if __name__ == '__main__':

    # noinspection PyBroadException
    try:

        # ---------------------------------------------------------------------
        # 입력 받을 변수
        #
        # 1. 로그레벨
        #   1) 레벨 값 : D:DEBUG, E:ERROR, 그 외:INFO
        #
        # 2. 매수금액
        #   1) M : 수수료를 제외한 최대 가능 금액으로 매수
        #   2) 금액 : 입력한 금액만 매수(수수료 포함)
        #
        # 3. 매수 제외종목
        #   1) 종목코드(콤마구분자) : BTC,ETH
        # ---------------------------------------------------------------------

        # 1. 로그레벨
        log_level = "INFO"
        buy_amt = 5000

        upbit.set_loglevel(log_level)

        logging.info("*********************************************************")
        logging.info("1. 로그레벨 : " + str(log_level))
        logging.info("2. 매수금액 : " + str(buy_amt))
        logging.info("*********************************************************")

        # 매수 로직 시작
        start_buytrade(buy_amt)

    except KeyboardInterrupt:
        # 프로그램 종료 메세지 조립
        message = '\n\n[🚨❌🚨종료🚨❌🚨]'
        message = message + '\n\n buy_bot 종료!'
        message = message + '\n\n- 현재시간:' + str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
        # 프로그램 종료 메세지 발송
        upbit.send_telegram_message(message)
        
        logging.error("KeyboardInterrupt Exception 발생!")
        logging.error(traceback.format_exc())
        sys.exit(-100)

    except Exception:
        # 프로그램 종료 메세지 조립
        message = '\n\n[🚨❌🚨종료🚨❌🚨]'
        message = message + '\n\n buy_bot 종료!'
        message = message + '\n\n- 현재시간:' + str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
        # 프로그램 종료 메세지 발송
        upbit.send_telegram_message(message)
        
        logging.error("Exception 발생!")
        logging.error(traceback.format_exc())
        sys.exit(-200)