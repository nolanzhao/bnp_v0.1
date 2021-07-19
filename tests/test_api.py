import tushare as ts
from bnp.settings import cfg  # noqa

ts.set_token(cfg.BASE.TUSHARE_TOKEN)
pro = ts.pro_api()

df = pro.daily(ts_code='000001.SZ', start_date='20201116', end_date='20201116')
print(df.shape[0])


df = pro.daily(ts_code='000001.SZ', start_date='20201117', end_date='20201117')
print(df.shape[0])