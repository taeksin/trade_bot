import sys
import logging
import traceback

from module import upbit

# -----------------------------------------------------------------------------
# - Name : main
# - Desc : 메인
# -----------------------------------------------------------------------------
if __name__ == '__main__':

    # noinspection PyBroadException
    try:
        # 로그레벨 설정(DEBUG)
        upbit.set_loglevel('I')

        # 라인 메세지 발송
        rtn = upbit.send_line_message('테스트 메시지 입니다.')

        # 발송결과
        logging.info(rtn)

    except KeyboardInterrupt:
        logging.error("KeyboardInterrupt Exception 발생!")
        logging.error(traceback.format_exc())
        sys.exit(-100)

    except Exception:
        logging.error("Exception 발생!")
        logging.error(traceback.format_exc())
        sys.exit(-200)