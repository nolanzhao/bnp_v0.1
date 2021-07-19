from datetime import datetime, timedelta

import tushare as ts
from bnp.settings import cfg

ts.set_token(cfg.BASE.TUSHARE_TOKEN)
pro = ts.pro_api()


def today_str():
    t = datetime.today()
    return t.strftime('%Y-%m-%d')


def date_range(start_date: str, end_date: str) -> list:
    dt1 = datetime.strptime(start_date, "%Y-%m-%d")
    dt2 = datetime.strptime(end_date, "%Y-%m-%d")
    delta = dt2 - dt1
    res = []
    for i in range(delta.days + 1):
        dt = dt1 + timedelta(days=i)
        res.append(dt.strftime('%Y-%m-%d'))
    return res


def get_next_n_trade_day(start_date: str, n=1, exchange='') -> list:
    dt = datetime.strptime(start_date, "%Y-%m-%d")
    dt += timedelta(days=1)
    start_date = dt.strftime('%Y-%m-%d').replace('-', '')
    end_date = today_str().replace('-', '')
    # print(start_date)
    # print(end_date)
    df = pro.trade_cal(exchange=exchange, start_date=start_date, end_date=end_date)
    # print(df)
    res = []
    count = 0
    for _, row in df.iterrows():
        if row['is_open'] == 0:
            continue
        # print(row['cal_date'])
        res.append(row['cal_date'])
        count += 1
        if count >= n:
            break
    return res


def get_trade_days(start_date: str = None, end_date: str = None) -> list:
    """
    start_date: 起始日期, 格式'2020-11-07'
    end_date: 终止日期, 格式'2020-11-07'， 默认为今天日期
    """
    if not start_date:
        return []
    if not end_date:
        end_date = today_str()

    start_date = start_date.replace('-', '')
    end_date = end_date.replace('-', '')
    df = pro.trade_cal(exchange='', start_date=start_date, end_date=end_date)
    # print(df)
    res = []
    for _, row in df.iterrows():
        if row['is_open'] == 0:
            continue
        trade_date = datetime.strptime(row['cal_date'], "%Y%m%d").strftime('%Y-%m-%d')
        res.append(trade_date)
    return res


def get_recent_n_trade_days(n=1, include_today=False):
    """
    获取最近n个交易日, n < 200
    """
    assert n < 200
    end_date = today_str()
    dt1 = datetime.strptime(end_date, "%Y-%m-%d")
    dt0 = dt1 - timedelta(days=1000)
    start_date = dt0.strftime('%Y-%m-%d')
    res = get_trade_days(start_date, end_date)
    if include_today is False and res[-1] == today_str():
        return res[-n-1:-1]
    return res[-n:]


def get_last_n_trade_days(n=1, end_date=None):
    """
    获取前n个交易日, n < 200
    """
    assert n < 200
    end_date = end_date or today_str()
    dt1 = datetime.strptime(end_date, "%Y-%m-%d")
    dt0 = dt1 - timedelta(days=1000)
    start_date = dt0.strftime('%Y-%m-%d')
    res = get_trade_days(start_date, end_date)
    return res[-n:]


def is_trade_day_today():
    dt_str = today_str().replace('-', '')
    df = pro.trade_cal(exchange='', start_date=dt_str, end_date=dt_str)
    return bool(df['is_open'].to_numpy()[-1] == 1)


def get_next_trade_day(date_str):
    """
    date_str: str, 格式: %Y-%m-%d
    获取下一个交易日, 格式: %Y-%m-%d
    超过了今天返回None
    """
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    dt += timedelta(days=1)
    start_date = dt.strftime('%Y-%m-%d').replace('-', '')
    end_date = today_str().replace('-', '')
    # print(start_date)
    # print(end_date)
    df = pro.trade_cal(start_date=start_date, end_date=end_date)
    # print(df)

    for _, row in df.iterrows():
        if row['is_open'] == 0:
            continue
        # print(row['cal_date'])
        result = f"{row['cal_date'][:4]}-{row['cal_date'][4:6]}-{row['cal_date'][6:8]}"
        # print(result)
        return result




if __name__ == '__main__':
    # print(today_str())
    # start_date = "2020-11-01"
    # end_date = "2020-11-15"
    # date_range(start_date, end_date)

    # print(get_trade_days(start_date, end_date))
    # print(get_next_n_trade_day('2020-11-04', 3))

    # print(is_trade_day_today())

    print(get_next_trade_day('2021-03-29'))
