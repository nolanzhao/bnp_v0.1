import time

import tushare as ts
from bnp.settings import cfg
from bnp.utils import get_recent_n_trade_days, send_dingding_error_msg  # noqa
from talib import SMA

ts.set_token(cfg.BASE.TUSHARE_TOKEN)
pro = ts.pro_api()


def main(stock_pool=cfg.STOCK.HSZZ):
    n_days = get_recent_n_trade_days(n=80, include_today=True)
    print(n_days[0], n_days[-1])
    start_date = n_days[0].replace('-', '')
    end_date = n_days[-1].replace('-', '')

    res = []
    N = len(stock_pool)
    for index, stock_code in enumerate(stock_pool):
        print(f'[{index}/{N}]🤖 {stock_code}')
        try:
            df = pro.daily(ts_code=stock_code, start_date=start_date, end_date=end_date)
            close = df['close'].to_numpy()[::-1]
            if close[-1] < 10:
                continue

            ma5 = SMA(close, timeperiod=5)
            ma10 = SMA(close, timeperiod=10)
            ma20 = SMA(close, timeperiod=20)
            ma60 = SMA(close, timeperiod=60)

            if ma5[-1] > ma10[-1] > ma20[-1] > ma60[-1] and (not ma5[-2] > ma10[-2] > ma20[-2] > ma60[-2]):
                print(f"🎁🎁🎁 {stock_code}")
                res.append(stock_code)
        except Exception:
            from traceback import print_exc
            msg = print_exc()
            print(msg)
            # send_dingding_error_msg(msg)

        finally:
            time.sleep(cfg.BASE.TUSHARE_SLEEP)

    return res
