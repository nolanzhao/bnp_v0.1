import os

import tushare as ts
from bnp.settings import cfg
from bnp.utils import cache, today_str
from pymongo import MongoClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(f"mysql://{cfg.MYSQL.USER}:{cfg.MYSQL.PASSWD}@{cfg.MYSQL.HOST}/{cfg.MYSQL.DB}")
session_obj = sessionmaker(bind=engine)
session = scoped_session(session_obj)

URI = f"mongodb://{cfg.MONGO.USERNAME}:{cfg.MONGO.PASSWORD}@{cfg.MONGO.HOST}:{cfg.MONGO.PORT}/{cfg.MONGO.DB}?authMechanism=SCRAM-SHA-1"  # noqa
client = MongoClient(URI)
db = client[cfg.MONGO.DB]


ts.set_token(cfg.BASE.TUSHARE_TOKEN)
pro = ts.pro_api()


@cache
def get_stock_by_date(trade_day: str, stock_code: str):
    sql = text(f"select * from stock_all where stock_code='{stock_code}' and state_dt='{trade_day}'")
    # print(sql)
    result = session.execute(sql)
    result = list(result)
    if len(result) == 0:
        return None
    data = result[0]
    # print(data)
    return data


def wraps_stock_data(data):
    state_dt, stock_code, open_, close, high, low, vol, amount, \
        pre_close, amt_change, pct_change, big_order_cntro, big_order_delt = data
    res = {
        'state_dt': state_dt,
        'stock_code': stock_code,
        'open_': open_,
        'close': close,
        'high': high,
        'low': low,
        'vol': vol,
        'amount': amount,
        'pre_close': pre_close,
        'amt_change': amt_change,
        'pct_change': pct_change,
        'big_order_cntro': big_order_cntro,
        'big_order_delt': big_order_delt
    }
    return res


def get_stock_by_dts(dts: list, stock_code: str):
    """
    获取单只股票的多个日期的行情
    """
    res = []
    for dt in dts:
        data = get_stock_by_date(dt, stock_code)
        res.append(data)
    return res


def get_stock_by_range(stock_code: str, start_date=None, end_date=None, table='stock_all'):
    """
    获取单只股票的日期范围内的行情
    """
    if end_date is None:
        end_date = today_str()
    sql = text(f"select state_dt, stock_code, open, close, high, low, vol, amount, pre_close, amt_change, pct_change, \
            big_order_cntro, big_order_delt from {table} where stock_code = '{stock_code}' and state_dt >= '{start_date}' \
                and state_dt < '{end_date}' order by state_dt;")
    # print(sql)
    result = session.execute(sql)
    data = list(result)
    # print(data)
    return data


def get_stock_name(code_):
    DATA_PATH = os.path.join(os.path.dirname(__file__), '../settings/HSZZ')
    with open(DATA_PATH, 'r') as f:
        for line in f.readlines():
            code, name = line.split()
            if code == code_:
                return name


def is_today_data_exists():
    dt = today_str().replace('-', '')
    df = pro.daily(ts_code='000001.SZ', start_date=dt, end_date=dt)
    return True if df.shape[0] == 1 else False


def get_stock_info(ts_code):
    # item = db.stock_info.find_one({'ts_code': ts_code})
    # return item
    data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,name,industry,market')
    items = data.query(f'ts_code=="{ts_code}"').to_dict('records')
    item = {}
    if len(items) > 0:
        item = items[0]
    return item


if __name__ == '__main__':
    # res = get_stock_by_range('000008.SZ', '2020-11-04')
    # print(res)
    item = get_stock_info("000799.SZ")
    print(item)
