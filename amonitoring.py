import logging
import sys
import time
import traceback
from datetime import datetime
from decimal import Decimal

from module import upbit


# -----------------------------------------------------------------------------
# - Name : start_mon
# - Desc : 모니터링 로직
# - Input
# - Output
# -----------------------------------------------------------------------------
def start_monitoring():
    try:

        # 프로그램 시작 메세지 발송
        message = '\n\n[프로그램 시작 안내]'
        message = message + '\n\n 모니터링이 시작 되었습니다!'
        message = message + '\n\n- 현재시간:' + str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))

        # 프로그램 시작 메세지 발송
        upbit.send_telegram_message(message)

        # ---------------------------------------------------------------------
        # 알림 발송 용 변수
        # ---------------------------------------------------------------------
        sent_list = []
        # ---------------------------------------------------------------------

        # 반복 조회
        while True:

            # ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
            # 전일대비
            
            # -----------------------------------------------------------------
            # 전체 종목 리스트 추출
            # -----------------------------------------------------------------
            target_items = upbit.get_items('KRW', '')
            for target_item in target_items:
                time.sleep(0.3)
                change_rate,trade_price = upbit.get_change_rate(target_item['market'])
                float(change_rate)
                # 개별 종목 10% 이상 상승 시 메세지 발송(1시간 간격)
                if change_rate >= 10:
                    logging.info("PCNT-UP 조건 만족![" + str(target_item['market']) + "]")
                    logging.info("변동률: [" + str(change_rate) + "% ]")

                    # 알림 Key 조립
                    msg_key = {'TYPE': 'PCNT-UP','ITEM': target_item['market']}

                    # 메세지 조립
                    message = '\n\n[🔺상승!🔺]'
                    message = message + '\n\n- 종목: ' +str(target_item['market'])
                    message = message + '\n- 현재가: ' + str(trade_price)
                    message = message + '\n- 변동률:  ' + str('%.2f' % float(change_rate)) + "%"

                    # 메세지 발송(2시간:7200초 간격)
                    sent_list = upbit.send_msg(sent_list, msg_key, message, '7200')

                # 개별 종목 10% 이상 하락 시 메세지 발송(1시간 간격)
                if change_rate <= -10:
                    logging.info("PCNT-DOWN 조건 만족![" + str(target_item['market']) + "]")
                    logging.info("변동률: [" + str(change_rate) + "% ]")

                    # 알림 Key 조립
                    msg_key = {'TYPE': 'PCNT-UP','ITEM': target_item['market']}

                    # 메세지 조립
                    message = '\n\n[💙하락!💙]'
                    message = message + '\n\n- 종목: ' + str(target_item['market'])
                    message = message + '\n- 현재가: ' + str(trade_price)
                    message = message + '\n- 변동률:  ' + str('%.2f' % float(change_rate)) + "%"

                    # 메세지 발송(2시간:7200초 간격)
                    sent_list = upbit.send_msg(sent_list, msg_key, message, '7200')
    # ----------------------------------------
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
        # 로그레벨 설정(DEBUG)
        upbit.set_loglevel('I')

        # 모니터링 프로그램 시작
        start_monitoring()

    except KeyboardInterrupt:
        # 프로그램 종료 메세지 조립
        message = '\n\n[🚨❌🚨종료🚨❌🚨]'
        message = message + '\n\n 모니터링이 종료!'
        message = message + '\n\n- 현재시간:' + str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
        # 프로그램 종료 메세지 발송
        upbit.send_telegram_message(message)
        
        logging.error("KeyboardInterrupt Exception 발생!")
        logging.error(traceback.format_exc())
        sys.exit(-100)

    except Exception:
         # 프로그램 종료 메세지 조립
        message = '\n\n[🚨❌🚨종료🚨❌🚨]'
        message = message + '\n\n 모니터링이 종료!'
        message = message + '\n\n- 현재시간:' + str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
        # 프로그램 종료 메세지 발송
        upbit.send_telegram_message(message)
        
        logging.error("Exception 발생!")
        logging.error(traceback.format_exc())
        sys.exit(-200)
