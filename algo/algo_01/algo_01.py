import time  # noqa
# from decimal import Decimal
from traceback import print_exc  # noqa

from bnp.settings import cfg
# from bnp.utils import send_dingding_error_msg
from pymongo import ASCENDING, MongoClient

URI = f"mongodb://{cfg.MONGO.USERNAME}:{cfg.MONGO.PASSWORD}@{cfg.MONGO.HOST}:{cfg.MONGO.PORT}/{cfg.MONGO.DB}?authMechanism=SCRAM-SHA-1"  # noqa
client = MongoClient(URI)
db = client[cfg.MONGO.DB]
collection_name = 'recent_03_days'
_c = db[collection_name]


def search(stock_code, start_date=None):
    data = _c.find({'stock_code': stock_code, 'state_dt': {'$gte': start_date}}).sort([("state_dt", ASCENDING)])
    data = [item for item in data]

    assert len(data) >= 3
    day0, day1, day2 = data[0], data[1], data[2]

    if day0['pct_change'] > 9:
        if day1['close'] < day1['pre_close'] and day2['close'] < day2['pre_close']:
            if day0['vol'] * 1.5 > day1['vol'] and day1['vol'] > day2['vol']:
                print(f'haha! {stock_code}')
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
        try:
            target_code = search(stock_code, start_date=start_date)
            if target_code is not None:
                # print(f"🎁🎁🎁 {target_code}")
                res.append(target_code)

        except Exception:
            msg = print_exc()
            print(msg)
            # send_dingding_error_msg(msg)
            print(f'👾👾👾 {stock_code} ERROR!')

    return res


if __name__ == '__main__':
    _STOCK_POOL = cfg.STOCK.HSZZ
    _START_DATE = '2020-11-11'
    main(stock_pool=_STOCK_POOL, start_date=_START_DATE)
