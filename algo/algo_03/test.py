import numpy as np
import tushare as ts
from bnp.settings import cfg
from bnp.utils import get_recent_n_trade_days
from talib import *  # noqa

ts.set_token(cfg.BASE.TUSHARE_TOKEN)
pro = ts.pro_api()


n_days = get_recent_n_trade_days(n=100, include_today=True)
print(n_days[0], n_days[-1])
start_date = n_days[0].replace('-', '')
end_date = n_days[-1].replace('-', '')

df = pro.daily(ts_code='002594.SZ', start_date=start_date, end_date=end_date)
print(df)

open = df['open'].to_numpy()[::-1]
high = df['high'].to_numpy()[::-1]
low = df['low'].to_numpy()[::-1]
close = df['close'].to_numpy()[::-1]

integer = CDL3INSIDE(open, high, low, close)  # noqa
print(integer)

print("*****************")
item = np.nonzero(integer)[0]
print(item)
for ind in item:
    # sign = '+' if integer[ind] > 0 else '-'
    print(integer[ind], n_days[ind])