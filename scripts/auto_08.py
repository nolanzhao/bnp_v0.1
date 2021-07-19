from datetime import datetime

from bnp.algo.algo_08 import search_target  # noqa
from bnp.settings import cfg  # noqa
from bnp.utils import (get_stock_info, is_trade_day_today, save_record, send_dingding_msg, send_mail, today_str)

if is_trade_day_today() is False:
    print('今天不是交易日.')
    exit()

_STOCK_POOL = cfg.STOCK.A3974

start_time = datetime.now()

# step 1. search
print('## 准备搜索目标...')
res = search_target(stock_pool=_STOCK_POOL)

L = []
for ts_code, _ in res:
    try:
        item = get_stock_info(ts_code)
        print(item['ts_code'], item['name'], item['industry'], item['market'])
        L.append({'ts_code': item['ts_code'], 'name': item['name'], 'industry': item['industry'], 'market': item['market']})
    except Exception:
        pass

# step 2. save result to mongo
save_record(L, algo="algo_08")

# step 3. send dingding
msg = {'date': today_str(), 'stocks': L, 'algo': '算法8#A3974'}
# send_dingding_msg(msg)
send_mail(msg)

end_time = datetime.now()
print(f"日期: {today_str()}")
print(f"耗时: {end_time - start_time}")
print('🎉🎉🎉 All Finished!')
