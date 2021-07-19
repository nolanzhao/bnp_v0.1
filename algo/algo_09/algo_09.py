import time

import tushare as ts
from bnp.settings import cfg  # noqa
from bnp.utils import get_recent_n_trade_days, send_dingding_error_msg, get_last_n_trade_days  # noqa
from talib import *  # noqa

ts.set_token(cfg.BASE.TUSHARE_TOKEN)
pro = ts.pro_api()


def is_gentle_rise(open, close):
    if 0 < (close - open) / open <= 0.03:
        return True
    return False


def check(df):
    ts_code = df['ts_code'].to_numpy()[::-1][-1]
    close = df['close'].to_numpy()[::-1]
    open = df['open'].to_numpy()[::-1]
    pct_chg = df['pct_chg'].to_numpy()[::-1]
    vol = df['vol'].to_numpy()[::-1]

    F1, F2 = False, False
    # 5天内有4天是小阳线
    cnt = 0
    for i in range(5):
        if is_gentle_rise(open[i], close[i]):
            cnt += 1
    if cnt >= 4:
        F1 = True

    # 温和放量
    if vol[-4] > vol[-5] and vol[-3] > (vol[-4] + vol[-5]) / 2 and vol[-2] > (vol[-3] + vol[-4] + vol[-5]) / 3 and vol[-1] > (
            vol[-2] + vol[-3] + vol[-4] + vol[-5]) / 4:
        F2 = True

    return F1 and F2


def search(stock_code, n_days=None, mode=1):
    assert n_days is not None
    # print(n_days[0], n_days[-1])
    start_date = n_days[0].replace('-', '')
    end_date = n_days[-1].replace('-', '')

    # print(stock_code, start_date, end_date)
    df = pro.daily(ts_code=stock_code, start_date=start_date, end_date=end_date)
    # print(df)

    if len(df) < 5:
        # print(f"{stock_code} {n_days} 数据不够5天")
        return False

    res = check(df)
    # print("res: ", res)
    return res


def main(stock_pool=cfg.STOCK.HSZZ, end_date=None, verbose=True):
    if end_date is None:
        n_days = get_recent_n_trade_days(n=5, include_today=True)
    else:
        n_days = get_last_n_trade_days(n=5, end_date=end_date)

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
                res.append((stock_code, 'algo_09'))

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
    main(end_date="2021-04-22")
