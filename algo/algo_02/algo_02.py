import time  # noqa
# from decimal import Decimal
from traceback import print_exc  # noqa

from bnp.settings import cfg
from bnp.utils import get_recent_n_trade_days, send_dingding_error_msg  # noqa
from pymongo import ASCENDING, MongoClient

URI = f"mongodb://{cfg.MONGO.USERNAME}:{cfg.MONGO.PASSWORD}@{cfg.MONGO.HOST}:{cfg.MONGO.PORT}/{cfg.MONGO.DB}?authMechanism=SCRAM-SHA-1"  # noqa
client = MongoClient(URI)
db = client[cfg.MONGO.DB]
collection_name = "recent_21_days"
_c = db[collection_name]


def search(stock_code, start_date):
    # print(trade_days)
    data = _c.find({'stock_code': stock_code, 'state_dt': {'$gte': start_date}}).sort([("state_dt", ASCENDING)])
    data = [item for item in data]

    # assert len(data) == 21
    last_day = data[-1]
    max_pre20 = max([item['high'] for item in data[:-1]])
    if last_day['close'] > max_pre20:
        return stock_code


def main(stock_pool=None, start_date=None):
    assert stock_pool is not None
    assert start_date is not None
    # print(stock_pool)
    res = []
    N = len(stock_pool)
    for index, stock_code in enumerate(stock_pool):
        print(f'[{index}/{N}]🤖 {stock_code}')
        try:
            target_code = search(stock_code, start_date)
            if target_code is not None:
                # print(f"🎁🎁🎁 {target_code}")
                res.append(target_code)

        except Exception:
            msg = print_exc()
            print(msg)
            # send_dingding_error_msg(msg)
            print(f'👾👾👾 {stock_code} ERROR!')

    # print(res)
    return res


if __name__ == '__main__':
    _STOCK_POOL = cfg.STOCK.HSZZ
    trade_days = get_recent_n_trade_days(21)
    res = main(stock_pool=_STOCK_POOL, start_date=trade_days[0])

    for ts_code in res:
        item = db.stock_info.find_one({'ts_code': ts_code})
        print(item['ts_code'], item['name'], item['industry'], item['market'])
