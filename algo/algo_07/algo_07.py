import time

import tushare as ts
from bnp.settings import cfg
from bnp.utils import get_recent_n_trade_days, send_dingding_error_msg  # noqa

ts.set_token(cfg.BASE.TUSHARE_TOKEN)
pro = ts.pro_api()


def main(stock_pool=cfg.STOCK.HSZZ):
    n_days = get_recent_n_trade_days(n=120, include_today=True)
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
            high = df['high'].to_numpy()[::-1]
            pre_max = max(high[:-1])

            if close[-1] > pre_max:
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
