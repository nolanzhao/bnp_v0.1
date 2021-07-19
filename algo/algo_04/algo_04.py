import time

import tushare as ts
from bnp.settings import cfg  # noqa
from bnp.utils import get_recent_n_trade_days, send_dingding_error_msg  # noqa
from talib import *  # noqa

ts.set_token(cfg.BASE.TUSHARE_TOKEN)
pro = ts.pro_api()


def search(stock_code, n_days=None, mode=1):
    assert n_days is not None
    # print(n_days[0], n_days[-1])
    start_date = n_days[0].replace('-', '')
    end_date = n_days[-1].replace('-', '')

    df = pro.daily(ts_code=stock_code, start_date=start_date, end_date=end_date)
    vol = df['vol'].to_numpy()[::-1]
    close = df['close'].to_numpy()[::-1]
    open = df['open'].to_numpy()[::-1]

    if mode == 1:
        if open[-1] > close[-1]:
            return False
        avg3 = sum(vol[-4:-1]) / 3
        avg10 = sum(vol[-11:-1]) / 10
        if vol[-1] > 3 * avg3 and vol[-1] > 3 * avg10:
            # print(vol[-1], sum(vol[-4:-1]) / 3)
            return True
    elif mode == 2:
        if open[-1] > close[-1] or open[-2] > close[-2]:
            return False
        avg3 = sum(vol[-5:-2]) / 3
        avg10 = sum(vol[-12:-2]) / 10
        if vol[-2] > 3 * avg3 and vol[-2] > 3 * avg10 and vol[-1] > vol[-2] * 0.95:
            return True
    elif mode == 3:
        if open[-1] > close[-1] or open[-2] > close[-2] or open[-3] > close[-3]:
            return False
        avg3 = sum(vol[-6:-3]) / 3
        avg10 = sum(vol[-13:-3]) / 10
        if vol[-3] > 3 * avg3 and vol[-3] > 3 * avg10 and vol[-2] > vol[-3] * 0.95 and vol[-1] > vol[-3] * 0.95:
            return True

    return False


def main(stock_pool=cfg.STOCK.HSZZ):
    n_days = get_recent_n_trade_days(n=20, include_today=True)

    res = []
    N = len(stock_pool)
    for index, stock_code in enumerate(stock_pool):
        print(f'[{index}/{N}]🤖 {stock_code}')
        try:
            is_target_01 = search(stock_code, n_days=n_days, mode=1)
            if is_target_01 is True:
                print(f"🎁🎁🎁 单日模式: {stock_code}")
                res.append((stock_code, '单日模式'))
            # is_target_02 = search(stock_code, n_days=n_days, mode=2)
            # if is_target_02 is True:
            #     print(f"🎁🎁🎁 双日模式: {stock_code}")
            #     res.append((stock_code, '双日模式'))
            # is_target_03 = search(stock_code, n_days=n_days, mode=3)
            # if is_target_03 is True:
            #     print(f"🎁🎁🎁 三日模式: {stock_code}")
            #     res.append((stock_code, '三日模式'))

        except Exception:
            from traceback import print_exc
            msg = print_exc()
            print(msg)
            # send_dingding_error_msg(msg)
            print(f'👾👾👾 {stock_code} ERROR!')

        finally:
            time.sleep(cfg.BASE.TUSHARE_SLEEP)

    print(f"## res: {res}")
    return res


if __name__ == '__main__':
    _STOCK_POOL = cfg.STOCK.HSZZ
    main(stock_pool=_STOCK_POOL)
