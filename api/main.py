"""
alpha_stock软件的API
"""
import datetime
from collections import defaultdict

import pytz
import tushare as ts
from bnp.settings import cfg
from bnp.utils import get_recent_n_trade_days
import bson
from bson import ObjectId
from bson.json_util import dumps, loads
from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient

utc = pytz.UTC

ts.set_token(cfg.BASE.TUSHARE_TOKEN)
pro = ts.pro_api()

URI = f"mongodb://{cfg.MONGO.USERNAME}:{cfg.MONGO.PASSWORD}@{cfg.MONGO.HOST}:{cfg.MONGO.PORT}/{cfg.MONGO.DB}?authMechanism=SCRAM-SHA-1"  # noqa
client = MongoClient(URI)
db = client[cfg.MONGO.DB]


class RecommendItem(BaseModel):
    date: str
    algo: int


class StatisticItem(BaseModel):
    date: str
    days: int


class ExpectationItem(BaseModel):
    algo: int


class TokenItem(BaseModel):
    token: str


app = FastAPI()

algo_list = [('algo_01', '先涨后跌'), ('algo_03', 'K线形态识别'), ('algo_04', '成交量放大'), ('algo_05', 'MACD金叉'), ('algo_06', '多头排列'),
             ('algo_07', '突破120日高点')]


def rank(days):
    if days == 1:
        n_days = get_recent_n_trade_days(n=days, include_today=True)
        # print(n_days)
        d = defaultdict(list)
        for algo, description in algo_list:
            items = db.record.find({'date': n_days[0], 'algo': algo})
            for item in items:
                # print(item)
                for stock in item['stocks']:
                    d[(stock['ts_code'], stock['name'])].append(description)

        d_ = sorted(d.items(), key=lambda x: -len(x[1]))
        d_ = [item for item in d_ if len(item[1]) >= 2]
        return d_, n_days

    elif days > 1:
        n_days = get_recent_n_trade_days(n=days, include_today=True)
        # print(n_days)
        d = defaultdict(int)
        for dt in n_days:
            items = db.record.find({'date': dt})
            for item in items:
                # print(item)
                for stock in item['stocks']:
                    d[(stock['ts_code'], stock['name'])] += 1

        d_ = sorted(d.items(), key=lambda x: -x[1])
        d_ = [item for item in d_ if item[1] >= 2]
        return d_, n_days
    else:
        return None, None


def calc_expectation(algo):
    n_days = get_recent_n_trade_days(n=3, include_today=True)
    recommend_day, buy_day, sell_day = n_days[0], n_days[1], n_days[2]
    # print('recommend_day:', recommend_day)
    # print('buy_day:', buy_day)
    # print('sell_day:', sell_day)
    cursor = db.record.find_one({'date': recommend_day, 'algo': algo})
    if cursor is None:
        return None, n_days
    # stock_codes = [stock['ts_code'] for stock in cursor['stocks']]
    # print('recommend_stocks:', stock_codes)
    if cursor is None:
        return None, n_days

    d_ = []
    for stock in cursor['stocks']:
        ts_code = stock['ts_code']
        # print(ts_code)
        start_date = buy_day.replace('-', '')
        end_date = sell_day.replace('-', '')
        df = pro.daily(ts_code=ts_code, start_date=start_date, end_date=end_date)

        open = df['open'].to_numpy()[::-1]
        close = df['close'].to_numpy()[::-1]
        high = df['high'].to_numpy()[::-1]
        low = df['low'].to_numpy()[::-1]

        if len(open) != 2:
            return None, n_days

        # 注： 推荐当天未第0天
        day1_open = open[0]  # 推荐后的第1天开盘价买
        day1_high = high[0]  # 推荐后的第1天开盘价买
        day1_low = low[0]  # 推荐后的第1天开盘价买
        day2_open = open[1]  # 推荐后的第2天开盘价卖
        day2_close = close[1]  # 推荐后的第2天收盘价卖
        day2_high = high[1]  # 推荐后的第2天最高价卖
        day2_low = low[1]  # 推荐后的第2天最低价卖

        regular_open_profit = (day2_open - day1_open) / day1_open
        regular_close_profit = (day2_close - day1_open) / day1_open
        regular_high_profit = (day2_high - day1_open) / day1_open
        regular_low_profit = (day2_low - day1_open) / day1_open

        probable_open_high_profit = ((day2_open + day2_high) / 2 - day1_open) / day1_open
        probable_open_close_profit = ((day2_open + day2_close) / 2 - day1_open) / day1_open
        probable_high_low_profit = ((day2_high + day2_low) / 2 - day1_open) / day1_open

        extream_high_profit = (day2_high - day1_low) / day1_low
        extream_low_profit = (day2_low - day1_high) / day1_high

        # print(regular_open_profit, regular_close_profit, regular_high_profit, regular_low_profit)
        # print(probable_open_high_profit, probable_open_close_profit, probable_high_low_profit)
        # print(extream_high_profit, extream_low_profit)

        d_.append([
            stock['ts_code'], stock['name'], regular_open_profit, regular_close_profit, regular_high_profit, regular_low_profit,
            probable_open_high_profit, probable_open_close_profit, probable_high_low_profit, extream_high_profit,
            extream_low_profit
        ])
    return d_, n_days


@app.post("/api/stock/verify_token")
def verify_token(item: TokenItem):
    if not bson.objectid.ObjectId.is_valid(item.token):
        return False
    data = db.account.find_one({'_id': ObjectId(item.token)})
    if data is None:
        return False
    if int(data['validity']) == -1:
        return True
    deadline = data['_id'].generation_time + datetime.timedelta(hours=8) + datetime.timedelta(days=int(data['validity']))
    return utc.localize(datetime.datetime.utcnow()) < deadline


@app.post("/api/stock/recommend")
async def recommend(item: RecommendItem):
    dt = item.date
    algo = f'algo_{str(item.algo).zfill(2)}'
    cursor = db.record.find_one({'date': dt, 'algo': algo})
    records = loads(dumps(cursor))
    if records is not None:
        del records['_id']
    return records


@app.post("/api/stock/statistic")
async def statistic(item: StatisticItem):
    days = item.days
    d_, n_days = rank(days)
    data = {
        'n_days': n_days,
        'd_': d_,
    }
    return data


@app.post("/api/stock/expectation")
async def expectation(item: ExpectationItem):
    algo = item.algo
    algo = f'algo_{str(item.algo).zfill(2)}'
    # print(algo)
    d_, n_days = calc_expectation(algo)
    data = {
        'algo': algo,
        'n_days': n_days,
        'd_': d_,
    }
    return data
