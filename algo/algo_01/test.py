import time  # noqa
from decimal import Decimal
from bnp.settings import cfg
from pymongo import MongoClient, ASCENDING

URI = f"mongodb://{cfg.MONGO.USERNAME}:{cfg.MONGO.PASSWORD}@{cfg.MONGO.HOST}:{cfg.MONGO.PORT}/{cfg.MONGO.DB}?authMechanism=SCRAM-SHA-1"  # noqa
client = MongoClient(URI)
db = client[cfg.MONGO.DB]


def cal_profit(day1, day2):
    buy_price = day1['close']
    sell_price = (day2['high'] + day2['low']) / 2
    # sell_price = day2['high']
    profit = (sell_price - buy_price) / buy_price
    profit = Decimal(profit).quantize(Decimal("0.0000"))
    return profit, buy_price, sell_price


def search(stock_code, start_date, end_date):
    data = db.backtest.find({
        'stock_code': stock_code,
        'state_dt': {
            '$gte': start_date,
            '$lte': end_date
        }
    }).sort([("state_dt", ASCENDING)])
    # print(data)
    data = [item for item in data]
    for i in range(len(data) - 4):
        day0, day1, day2, day3, day4 = data[i], data[i + 1], data[i + 2], data[i + 3], data[i + 4]
        # print(day0['state_dt'])
        # print(day1['state_dt'])
        # print(day2['state_dt'])
        # print(day3['state_dt'])
        # print(day4['state_dt'])
        # input()
        # 首日上涨9%以上
        if day0['pct_change'] > 9:
            # 连跌3天
            if day1['close'] < day1['pre_close'] and day2['close'] < day2['pre_close'] and day3['close'] < day3['pre_close']:
                # 每次下跌都是缩量
                if day0['vol'] * 1.5 > day1['vol'] and day1['vol'] > day2['vol'] and day2['vol'] > day3['vol']:
                    # print(f'haha! {stock_code} {res0[0]}')
                    profit, buy_price, sell_price = cal_profit(day3, day4)
                    res = {
                        'stock_code': stock_code,
                        'profit': profit,
                        'buy_dt': day3['state_dt'],
                        'buy_price': buy_price,
                        'sell_dt': day4['state_dt'],
                        'sell_price': sell_price
                    }
                    return res


def main(stock_pool, start_date, end_date):
    captial = Decimal(10)
    possible_profit = 0
    pos, neg, total = 0, 0, 0
    min_profit = 0
    max_profit = 0
    N = len(stock_pool)
    for index, stock_code in enumerate(stock_pool):
        # print(stock_code)
        try:
            res = search(stock_code, start_date, end_date)
            if res is not None:
                print(f"[{index}/{N}] 💷 {res}")
                min_profit = min(min_profit, res['profit'])
                max_profit = max(max_profit, res['profit'])
                possible_profit += captial * res['profit']
                total += 1
                if res['profit'] > 0:
                    pos += 1
                else:
                    neg += 1
                assert total == pos + neg

        except Exception as e:
            print(e)
            print(f'👾👾👾 {stock_code} ERROR!')

    if total == 0:
        return
    print(f"💰💰💰 总收益: {possible_profit}")
    print(f"💰💰💰 单日最小收益率: {min_profit}")
    print(f"💰💰💰 单日最大收益率: {max_profit}")
    print(f"💰💰💰 总交易次数: {total}")
    print(f"💰💰💰 正收益次数: {pos}")
    pos_ratio = pos / total
    print(f"💰💰💰 正确率: {pos_ratio}")


if __name__ == '__main__':
    _STOCK_POOL = cfg.STOCK.HSZZ
    _START_DATE = '2021-02-20'
    _END_DATE = '2021-03-26'

    main(stock_pool=_STOCK_POOL, start_date=_START_DATE, end_date=_END_DATE)
