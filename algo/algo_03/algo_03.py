import numpy as np
from bnp.settings import cfg  # noqa
from bnp.utils import today_str, send_dingding_error_msg  # noqa
from pymongo import ASCENDING, MongoClient
from talib import *  # noqa

URI = f"mongodb://{cfg.MONGO.USERNAME}:{cfg.MONGO.PASSWORD}@{cfg.MONGO.HOST}:{cfg.MONGO.PORT}/{cfg.MONGO.DB}?authMechanism=SCRAM-SHA-1"  # noqa
client = MongoClient(URI)
db = client[cfg.MONGO.DB]
collection_name = "recent_15_days"
_c = db[collection_name]

ALGO_LIST = [
    'CDL3INSIDE',
    'CDL3OUTSIDE',
    'CDL3STARSINSOUTH',
    'CDL3WHITESOLDIERS',
    'CDLMORNINGDOJISTAR',  # 3
    'CDLMORNINGSTAR',  # 3
    'CDLCONCEALBABYSWALL',  # 4
    'CDLBREAKAWAY',  # 5
    'CDLLADDERBOTTOM',  # 5
    'CDLRISEFALL3METHODS',  # 5
    'CDLXSIDEGAP3METHODS',  # 5
]


def need_param_penetration(algo):
    L = [
        'CDLMORNINGDOJISTAR',
        'CDLMORNINGSTAR',
    ]
    if algo in L:
        return True
    return False


def search(stock_code, start_date=None, algo=None):
    data = _c.find({
        'stock_code': stock_code,
        'state_dt': {
            '$gte': start_date,
        }
    }).sort([("state_dt", ASCENDING)])
    data = [item for item in data]

    last_date = data[-1]['state_dt']

    open = np.array([item['open'] for item in data])
    high = np.array([item['high'] for item in data])
    low = np.array([item['low'] for item in data])
    close = np.array([item['close'] for item in data])

    func = eval(algo)
    if not need_param_penetration(algo):
        integer = func(open, high, low, close)
    else:
        integer = func(open, high, low, close, penetration=0)

    item = np.nonzero(integer)[0]
    # print(item)
    if len(item) == 0:
        return None
    ind = item[-1]
    score = integer[ind]
    if data[ind]['state_dt'] != last_date or score < 0 or data[ind]['close'] < 10:
        return None
    return stock_code


def main(stock_pool=None, start_date=None):
    assert start_date is not None
    assert stock_pool is not None
    # print(start_date)
    # print(stock_pool)
    res = []
    N = len(stock_pool)
    for index, stock_code in enumerate(stock_pool):
        print(f'[{index}/{N}]🤖 {stock_code}')
        for algo in ALGO_LIST:
            try:
                target_code = search(stock_code, start_date=start_date, algo=algo)
                if target_code is not None:
                    # print(f"🎁🎁🎁 {target_code}")
                    res.append((target_code, algo))

            except Exception:
                from traceback import print_exc
                msg = print_exc()
                print(msg)
                # send_dingding_error_msg(msg)
                print(f'👾👾👾 {stock_code} ERROR!')

    return res


if __name__ == '__main__':
    _STOCK_POOL = cfg.STOCK.HSZZ
    # _STOCK_POOL = ['002594.SZ']
    main(stock_pool=_STOCK_POOL)
