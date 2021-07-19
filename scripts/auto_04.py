from datetime import datetime

from bnp.algo.algo_04 import search_target  # noqa
from bnp.settings import cfg  # noqa
from bnp.utils import init_db  # noqa
from bnp.utils import (get_stock_info, is_trade_day_today, save_record, send_dingding_msg, send_mail, today_str)

if is_trade_day_today() is False:
    print('今天不是交易日.')
    exit()

_STOCK_POOL = cfg.STOCK.HSZZ

start_time = datetime.now()

print('## 准备搜索目标...')
res = search_target(stock_pool=_STOCK_POOL)
print(res)

L = []
for ts_code, algo in res:
    try:
        item = get_stock_info(ts_code)
        print(item['ts_code'], item['name'], item['industry'], item['market'], algo)
        L.append({
            'ts_code': item['ts_code'],
            # 'algo': algo,
            'name': item['name'],
            'industry': item['industry'],
            'market': item['market']
        })
    except Exception as e:
        print(e)

# step 2. save result to mongo
save_record(L, algo="algo_04")

# step 3. send dingding
msg = {'date': today_str(), 'stocks': L, 'algo': '算法4: 成交量放大'}
# send_dingding_msg(msg)
send_mail(msg)

end_time = datetime.now()
print(f"日期: {today_str()}")
print(f"耗时: {end_time - start_time}")
print('🎉🎉🎉 All Finished!')
