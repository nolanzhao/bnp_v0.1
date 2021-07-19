from datetime import datetime

from bnp.algo.algo_01 import collection_name, search_target  # noqa
from bnp.settings import cfg  # noqa
from bnp.utils import (get_recent_n_trade_days, get_stock_info, init_db, is_today_data_exists, is_trade_day_today, save_record,
                       send_dingding_msg, today_str)

if is_trade_day_today() is False:
    print('今天不是交易日.')
    exit()

start_time = datetime.now()

# step 0: 判断接口是否已有当天数据
_DATA_TODAY_EXISTS = is_today_data_exists()
# print(_DATA_TODAY_EXISTS)

# step 1: init_db
if _DATA_TODAY_EXISTS:
    n_days = get_recent_n_trade_days(n=3, include_today=True)
    print(n_days)
else:
    n_days = get_recent_n_trade_days(n=3, include_today=False)
    print(n_days)

_START_DATE = n_days[0]
_STOCK_POOL = cfg.STOCK.HSZZ

init_db(_STOCK_POOL, start_dt=_START_DATE, collection_name=collection_name)

# step 2. search
print('## 准备搜索目标...')
res = search_target(stock_pool=_STOCK_POOL, start_date=_START_DATE)

L = []
for ts_code in res:
    try:
        item = get_stock_info(ts_code)
        print(item['ts_code'], item['name'], item['industry'], item['market'])
        L.append({'ts_code': item['ts_code'], 'name': item['name'], 'industry': item['industry'], 'market': item['market']})
    except Exception:
        pass

# step 3. save result to mongo
save_record(L, algo="algo_01")

# step 4. send dingding
msg = {'date': today_str(), 'stocks': L, 'algo': '算法1: 先涨后跌'}
send_dingding_msg(msg)

end_time = datetime.now()
print(f"日期列表: {n_days}")
print(f"耗时: {end_time - start_time}")
print('🎉🎉🎉 All Finished!')
