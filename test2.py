import time
import os
import sys
import logging
import traceback
import pandas as pd
import numpy
import dateutil.parser

from decimal import Decimal
from datetime import datetime

# 공통 모듈 Import
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from module import upbit

# -----------------------------------------------------------------------------
# - Name : start_selltrade
# - Desc : 매도 로직
# - Input
# 1) sell_pcnt : 매도 수익률
# 2) dcnt_pcnt : 고점대비 하락률
# -----------------------------------------------------------------------------


def start_selltrade(sell_pcnt, dcnt_pcnt):
    try:
        # 프로그램 시작 메세지 발송
        message = '\n\n[🟦🔵프로그램 시작 안내🔵🟦]'
        message = message + '\n\n sell_bot 시작 되었습니다!'
        message = message + '\n\n- 현재시간:' + str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))

        # 프로그램 시작 메세지 발송
        upbit.send_telegram_message(message)

        # ---------------------------------------------------------------------
        # 알림 발송 용 변수
        # ---------------------------------------------------------------------
        sent_list = []
        # ---------------------------------------------------------------------

        # ----------------------------------------------------------------------
        # 반복 수행
        # ----------------------------------------------------------------------
        while True:
            time.sleep(0.4)
            # ------------------------------------------------------------------
            # 보유 종목조회
            # ------------------------------------------------------------------
            target_items = upbit.get_accounts('Y', 'KRW')

            # ------------------------------------------------------------------
            # 보유 종목 현재가 조회
            # ------------------------------------------------------------------
            target_items_comma = upbit.chg_account_to_comma(target_items)
            tickers = upbit.get_ticker(target_items_comma)

            # -----------------------------------------------------------------
            # 보유 종목별 진행
            # -----------------------------------------------------------------
            for target_item in target_items:
                for ticker in tickers:
                    if target_item['market'] == ticker['market']:

                        # -------------------------------------------------
                        # 고점을 계산하기 위해 최근 매수일시 조회
                        # 1. 해당 종목에 대한 거래 조회(done, cancel)
                        # 2. 거래일시를 최근순으로 정렬
                        # 3. 매수 거래만 필터링
                        # 4. 가장 최근 거래일자부터 현재까지 고점을 조회
                        # -------------------------------------------------
                        order_done = upbit.get_order_status(target_item['market'], 'done') + upbit.get_order_status(target_item['market'], 'cancel')
                        order_done_sorted = upbit.orderby_dict(order_done, 'created_at', True)
                        order_done_filtered = upbit.filter_dict(order_done_sorted, 'side', 'bid')

                        # -------------------------------------------------
                        # 매수 직후 나타나는 오류 체크용 마지막 매수 시간 차이 계산
                        # -------------------------------------------------
                        # 마지막 매수 시간
                        last_buy_dt = datetime.strptime(dateutil.parser.parse(order_done_filtered[0]['created_at']).strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')

                        # 현재 시간 추출
                        current_dt = datetime.strptime(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')

                        # 시간 차이 추출
                        diff = current_dt - last_buy_dt

                        # 매수 후 1분간은 진행하지 않음(업비트 오류 방지 용)
                        if diff.seconds < 60:
                            logging.info('- 매수 직후 발생하는 오류를 방지하기 위해 진행하지 않음!!!')
                            logging.info('------------------------------------------------------')
                            continue

                        # -----------------------------------------------------
                        # 수익률 계산
                        # ((현재가 - 평균매수가) / 평균매수가) * 100
                        # -----------------------------------------------------
                        rev_pcnt = round(((Decimal(str(ticker['trade_price'])) - Decimal(str(target_item['avg_buy_price']))) / Decimal(str(target_item['avg_buy_price']))) * 100, 2)

                        logging.info('')
                        logging.info('------------------------------------------------------')
                        logging.info('- 종목:' + str(target_item['market']))
                        logging.info('- 평균매수가:' + str(target_item['avg_buy_price']))
                        logging.info('- 현재가:' + str(ticker['trade_price']))
                        logging.info('- 수익률:' + str(rev_pcnt))

                        # -----------------------------------------------------
                        # 현재 수익률이 매도 수익률 이상인 경우에만 진행
                        # -----------------------------------------------------
                        if Decimal(str(rev_pcnt)) < Decimal(str(sell_pcnt)):
                            logging.info('- 현재 수익률이 매도 수익률 보다 낮아 진행하지 않음!!!')
                            logging.info('------------------------------------------------------')
                            continue

                        # ------------------------------------------------------------------
                        # 캔들 조회
                        # ------------------------------------------------------------------
                        candles = upbit.get_candle(target_item['market'], '60', 200)

                        # ------------------------------------------------------------------
                        # 최근 매수일자 다음날부터 현재까지의 최고가를 계산
                        # ------------------------------------------------------------------
                        df = pd.DataFrame(candles)
                        mask = df['candle_date_time_kst'] > order_done_filtered[0]['created_at']
                        filtered_df = df.loc[mask]
                        highest_high_price = numpy.max(filtered_df['high_price'])

                        # -----------------------------------------------------
                        # 고점대비 하락률
                        # ((현재가 - 최고가) / 최고가) * 100
                        # -----------------------------------------------------
                        cur_dcnt_pcnt = round(((Decimal(str(ticker['trade_price'])) - Decimal(str(highest_high_price))) / Decimal(str(highest_high_price))) * 100, 2)

                        logging.info('- 매수 후 최고가:' + str(highest_high_price))
                        logging.info('- 고점대비 하락률:' + str(cur_dcnt_pcnt))
                        logging.info('- 최종 매수시간:' + str(last_buy_dt))

                        if Decimal(str(cur_dcnt_pcnt)) < Decimal(str(dcnt_pcnt)):

                            # ------------------------------------------------------------------
                            # 시장가 매도
                            # 실제 매도 로직은 안전을 위해 주석처리 하였습니다.
                            # 실제 매매를 원하시면 테스트를 충분히 거친 후 주석을 해제하시면 됩니다.
                            # ------------------------------------------------------------------
                            upbit.send_telegram_message("🟦🔵"+target_item['market']+"매도 대상 발견🔵🟦")
                            logging.info('시장가 매도 시작! [' + str(target_item['market']) + ']')
                            # rtn_sellcoin_mp = upbit.sellcoin_mp(target_item['market'], 'Y')
                            logging.info('시장가 매도 종료! [' + str(target_item['market']) + ']')
                            # logging.info(rtn_sellcoin_mp)
                            logging.info('------------------------------------------------------')
                            # ★ 매도 추천 메시지 보내기
                            # 알림 Key 조립
                            msg_key = {'TYPE': 'PCNT-UP','ITEM': target_item['market']}

                            # 메세지 조립
                            upbit.send_telegram_message("🟦🔵"+target_item['market']+"매도 대상 발견🔵🟦")
                            message = '\n\n[🟦🔵매도 추천 안내!🔵🟦]'
                            message = message + '\n\n- 종목: ' +str(target_item['market'])
                            message = message + '\n- 현재가: ' + str(target_item['trade_price'])
                            message = message + '\n- 현재 수익률: ' +Decimal(str(rev_pcnt))
                            message = message + '\n- 고점 대비 하락률: ' + str(cur_dcnt_pcnt)

                            # 메세지 발송(1시간:3600초 간격)
                            sent_list = upbit.send_msg(sent_list, msg_key, message, '3600')

                        else:
                            logging.info('- 고점 대비 하락률 조건에 맞지 않아 매도하지 않음!!!')
                            logging.info('------------------------------------------------------')

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
        # 2. 매도 수익률
        #   1) 2% = 2로 입력
        #
        # 3. 고점대비 하락률
        #   1) 1% = 1로 입력
        # ---------------------------------------------------------------------

        # 1. 로그레벨
        '''
        log_level = input("로그레벨(D:DEBUG, E:ERROR, 그 외:INFO) : ").upper()
        sell_pcnt = input("매도 수익률(ex:2%=2) : ")
        dcnt_pcnt = input("고점대비 하락률(ex:-1%=-1) : ")
        '''
        log_level = "INFO"
        sell_pcnt = 10
        dcnt_pcnt = -5
        upbit.set_loglevel(log_level)

        logging.info("*********************************************************")
        logging.info("1. 로그레벨 : " + str(log_level))
        logging.info("2. 매도 수익률 : " + str(sell_pcnt))
        logging.info("3. 고점대비 하락률 : " + str(dcnt_pcnt))
        logging.info("*********************************************************")

        # 매도 로직 시작
        start_selltrade(sell_pcnt, dcnt_pcnt)

    except KeyboardInterrupt:
        # 프로그램 종료 메세지 조립
        message = '\n\n[🚨❌🚨종료🚨❌🚨]'
        message = message + '\n\n sell_bot 종료!'
        message = message + '\n\n- 현재시간:' + str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
        # 프로그램 종료 메세지 발송
        upbit.send_telegram_message(message)
        
        logging.error("KeyboardInterrupt Exception 발생!")
        logging.error(traceback.format_exc())
        sys.exit(-100)

    except Exception:
        # 프로그램 종료 메세지 조립
        message = '\n\n[🚨❌🚨종료🚨❌🚨]'
        message = message + '\n\n sell_bot 종료!'
        message = message + '\n\n- 현재시간:' + str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
        # 프로그램 종료 메세지 발송
        upbit.send_telegram_message(message)
        
        logging.error("Exception 발생!")
        logging.error(traceback.format_exc())
        sys.exit(-200)
