import numpy as np
import tushare as ts
from bnp.settings import cfg
from bnp.utils import get_recent_n_trade_days
from talib import MACD
import time

ts.set_token(cfg.BASE.TUSHARE_TOKEN)
pro = ts.pro_api()

n_days = get_recent_n_trade_days(n=50, include_today=True)
print(n_days[0], n_days[-1])
start_date = n_days[0].replace('-', '')
end_date = n_days[-1].replace('-', '')

res = []
for stock_code in cfg.STOCK.HS300:
    df = pro.daily(ts_code=stock_code, start_date=start_date, end_date=end_date)
    close = df['close'].to_numpy()[::-1]
    macd, signal, hist = MACD(np.array(close), 12, 26, 9)

    if hist[-1] > 0 and np.diff(hist)[-1] > 0:
        print(stock_code)
        res.append(stock_code)

    time.sleep(0.2)


print(len(res))
