import time

import tushare as ts
from bnp.settings import cfg  # noqa
from bnp.utils import get_recent_n_trade_days, send_dingding_error_msg, get_last_n_trade_days  # noqa
from talib import *  # noqa

ts.set_token(cfg.BASE.TUSHARE_TOKEN)
pro = ts.pro_api()


def check(df, THRESHOLD=8.0):
    ts_code = df['ts_code'].to_numpy()[::-1][-1]
    # close = df['close'].to_numpy()[::-1]
    # open = df['open'].to_numpy()[::-1]
    pct_chg = df['pct_chg'].to_numpy()[::-1]
    # print(pct_chg)

    # day[-1]大涨
    f1 = bool(pct_chg[-1] >= THRESHOLD)

    # day[-2]没有大涨
    f2 = bool(pct_chg[-2] < THRESHOLD)

    # [ day[-7], day[-2] )有过大涨
    f3 = False
    for i in range(-7, -2):
        if pct_chg[i] >= THRESHOLD:
            f3 = True

    # print(f1, f2, f3)

    if (f1 is True) and (f2 is True) and (f3 is True):
        print(f"{ts_code} {pct_chg}")
        return True

    return False


def search(stock_code, n_days=None, mode=1):
    assert n_days is not None
    # print(n_days[0], n_days[-1])
    start_date = n_days[0].replace('-', '')
    end_date = n_days[-1].replace('-', '')

    # print(stock_code, start_date, end_date)
    df = pro.daily(ts_code=stock_code, start_date=start_date, end_date=end_date)
    # print(df)

    if len(df) < 7:
        # print(f"{stock_code} {n_days} 数据不够七天")
        return False

    res = check(df)
    # print("res: ", res)
    return res


def main(stock_pool=cfg.STOCK.ZZ1K, end_date=None, verbose=True):
    if end_date is None:
        n_days = get_recent_n_trade_days(n=7, include_today=True)
    else:
        n_days = get_last_n_trade_days(n=7, end_date=end_date)

    if verbose is True:
        print(n_days)

    res = []
    N = len(stock_pool)
    for index, stock_code in enumerate(stock_pool):        
        if verbose is True:
            print(f'[{index}/{N}]🤖 {stock_code}')
        try:
            is_target = search(stock_code, n_days=n_days, mode=1)

            if is_target is True:
                if verbose is True:
                    print(f"🎁🎁🎁 : {stock_code}")
                res.append((stock_code, 'algo_08'))

        except Exception:
            from traceback import print_exc
            msg = print_exc()
            if verbose is True:
                print(msg)
                # send_dingding_error_msg(msg)
                print(f'👾👾👾 {stock_code} ERROR!')

        finally:
            time.sleep(cfg.BASE.TUSHARE_SLEEP)

    if verbose is True:
        print(f"## res: {res}")
    return res


if __name__ == '__main__':
    main(end_date="2021-03-25")
