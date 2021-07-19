import time  # noqa
from decimal import Decimal
from bnp.settings import cfg
from bnp.utils import get_trade_days, get_last_n_trade_days, get_next_trade_day
from pymongo import MongoClient, ASCENDING
from bnp.algo.algo_08 import search_target

URI = f"mongodb://{cfg.MONGO.USERNAME}:{cfg.MONGO.PASSWORD}@{cfg.MONGO.HOST}:{cfg.MONGO.PORT}/{cfg.MONGO.DB}?authMechanism=SCRAM-SHA-1"  # noqa
client = MongoClient(URI)
db = client[cfg.MONGO.DB]


def verify(date_str, gift_stocks):
    dt_0 = get_next_trade_day(date_str)
    dt_1 = get_next_trade_day(dt_0)
    dt_2 = get_next_trade_day(dt_1)
    dt_3 = get_next_trade_day(dt_2)

    for stock_code, _ in gift_stocks:
        d0 = db.backtest_zz1k.find_one({
            'stock_code': stock_code,
            'state_dt': dt_0
        })

        d1 = db.backtest_zz1k.find_one({
            'stock_code': stock_code,
            'state_dt': dt_1
        })

        d2 = db.backtest_zz1k.find_one({
            'stock_code': stock_code,
            'state_dt': dt_2
        })

        d3 = db.backtest_zz1k.find_one({
            'stock_code': stock_code,
            'state_dt': dt_3
        })

        # print(f"[{stock_code} {dt_0}] open: {d0['open']} close: {d0['close']} high: {d0['high']} low: {d0['low']}")
        # print(f"[{stock_code} {dt_1}] open: {d1['open']} close: {d1['close']} high: {d1['high']} low: {d1['low']}")
        # print(f"[{stock_code} {dt_2}] open: {d2['open']} close: {d2['close']} high: {d2['high']} low: {d2['low']}")
        # print(f"[{stock_code} {dt_3}] open: {d3['open']} close: {d3['close']} high: {d3['high']} low: {d3['low']}")

        p1 = (d1['open'] - d0['open']) / d0['open'] * 100
        p1 = Decimal(p1).quantize(Decimal("0.0000"))

        p2 = (d2['open'] - d0['open']) / d0['open'] * 100
        p2 = Decimal(p2).quantize(Decimal("0.0000"))

        p3 = (d3['open'] - d0['open']) / d0['open'] * 100
        p3 = Decimal(p3).quantize(Decimal("0.0000"))

        if p1 > 0:
            profit = p1
        else:
            if p2 > 0:
                profit = p2
            else:
                profit = p3

        print(f"[{date_str} {stock_code} 💷 {profit}%]  {p1}%  {p2}%  {p3}%")

        with open('/home/nolan/Code/bnp/algo/algo_08/result.txt', 'a+') as f:
            f.write(f"[{date_str} {stock_code} 💷 {profit}%]  {p1}%  {p2}%  {p3}%\n")


def main(start_date, end_date):
    trade_days = get_trade_days(start_date, end_date)

    for date_str in trade_days:
        print(f"[🤖 {date_str}]")

        gift_stocks = search_target(stock_pool=cfg.STOCK.ZZ1K, end_date=date_str, verbose=False)
        # print(f"[{date_str}] 🎁🎁🎁 {gift_stocks}")

        verify(date_str, gift_stocks)


if __name__ == '__main__':
    main(start_date='2021-03-01', end_date='2021-04-01')

    # gift_stocks = [('300369.SZ', 'algo_08'), ('002474.SZ', 'algo_08'), ('605199.SH', 'algo_08'), ('603439.SH', 'algo_08'), ('300579.SZ', 'algo_08')]
    # verify('2021-03-25', gift_stocks)
