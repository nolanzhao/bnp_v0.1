import time  # noqa
from decimal import Decimal
from bnp.settings import cfg
from pymongo import MongoClient, ASCENDING

URI = f"mongodb://{cfg.MONGO.USERNAME}:{cfg.MONGO.PASSWORD}@{cfg.MONGO.HOST}:{cfg.MONGO.PORT}/{cfg.MONGO.DB}?authMechanism=SCRAM-SHA-1"  # noqa
client = MongoClient(URI)
db = client[cfg.MONGO.DB]


def cal_profit(day1, day2):
    buy_price = day1['open']
    sell_price = day2['open']
    # sell_price = (day2['high'] + day2['low']) / 2
    # if day2['open'] < 0:
    #     sell_price = day2['open']
    # else:
    #     sell_price = day2['close']
    profit = (sell_price - buy_price) / buy_price
    profit = Decimal(profit).quantize(Decimal("0.0000"))
    # print(f"profit: {profit * 100}%")
    return profit, buy_price, sell_price


def check_mode_1(open, close, vol):
    if open[-1] > close[-1]:
        return False
    avg3 = sum(vol[-4:-1]) / 3
    avg10 = sum(vol[-11:-1]) / 10
    if vol[-1] > 3 * avg3 and vol[-1] > 3 * avg10:
        return True
    return False


def check_mode_2(open, close, vol):
    if open[-1] > close[-1] or open[-2] > close[-2]:
        return False
    avg3 = sum(vol[-5:-2]) / 3
    avg10 = sum(vol[-12:-2]) / 10
    if vol[-2] > 3 * avg3 and vol[-2] > 3 * avg10 and vol[-1] > vol[-2] * 0.95:
        return True
    return False


def check_mode_3(open, close, vol):
    if open[-1] > close[-1] or open[-2] > close[-2] or open[-3] > close[-3]:
        return False
    avg3 = sum(vol[-6:-3]) / 3
    avg10 = sum(vol[-13:-3]) / 10
    if vol[-3] > 3 * avg3 and vol[-3] > 3 * avg10 and vol[-2] > vol[-3] * 0.95 and vol[-1] > vol[-3] * 0.95:
        return True
    return False


def check(data):
    open = [item['open'] for item in data]
    close = [item['close'] for item in data]
    vol = [item['vol'] for item in data]
    if check_mode_1(open, close, vol):
        return True
    return False


def search(stock_code, start_date, end_date):
    data = db.backtest.find({
        'stock_code': stock_code,
        'state_dt': {
            '$gte': start_date,
            '$lt': end_date
        }
    }).sort([("state_dt", ASCENDING)])
    # print(data)
    data = [item for item in data]
    for i in range(len(data) - 14):
        is_target = check(data[i:i + 13])
        if not is_target:
            continue

        day13, day14 = data[i + 13], data[i + 14]
        profit, buy_price, sell_price = cal_profit(day13, day14)
        res = {
            'stock_code': stock_code,
            'profit': profit,
            'buy_dt': day13['state_dt'],
            'buy_price': buy_price,
            'sell_dt': day14['state_dt'],
            'sell_price': sell_price
        }
        return res


def main(stock_pool, start_date, end_date):
    captial = Decimal(2000)  # 每次交易金额1W
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
                # print((f"[{str(index).rjust(3, '0')}/{N}]  💷 [{str(possible_profit).rjust(12, ' ')}]  💷 [{str(captial * res['profit']).rjust(12, ' ')}]  {res['stock_code']}  "
                #        f"{str(res['profit'] * 100).rjust(10, ' ')}%  {res['buy_dt']}  {str(res['buy_price']).rjust(6, ' ')}  "
                #        f"{res['sell_dt']}  {str(res['sell_price']).rjust(6, ' ')}"))
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
    print(f"💷 总净利润: {possible_profit}")
    print(f"💷 单日最小收益率: {min_profit * 100}%")
    print(f"💷 单日最大收益率: {max_profit * 100}%")
    print(f"💷 总交易次数: {total}")
    print(f"💷 正收益次数: {pos}")
    pos_ratio = pos / total
    print(f"💷 正确率: {pos_ratio * 100}%")


if __name__ == '__main__':
    _STOCK_POOL = cfg.STOCK.HSZZ
    # _START_DATE = '2021-01-20'
    # _END_DATE = '2021-03-26'

    DATE_RANGES = [
        ('2016-01-01', '2017-01-01'),
        ('2017-01-01', '2018-01-01'),
        ('2018-01-01', '2019-01-01'),
        ('2019-01-01', '2020-01-01'),
        ('2020-01-01', '2021-01-01'),
    ]

    for _START_DATE, _END_DATE in DATE_RANGES:
        print("\n\n")
        print(_START_DATE, _END_DATE)
        main(stock_pool=_STOCK_POOL, start_date=_START_DATE, end_date=_END_DATE)
