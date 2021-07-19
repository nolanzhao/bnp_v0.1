import datetime
import time

import tushare as ts
from bnp.settings import cfg
from pymongo import MongoClient
from bnp.utils import send_dingding_error_msg  # noqa

URI = f"mongodb://{cfg.MONGO.USERNAME}:{cfg.MONGO.PASSWORD}@{cfg.MONGO.HOST}:{cfg.MONGO.PORT}/{cfg.MONGO.DB}?authMechanism=SCRAM-SHA-1"  # noqa
client = MongoClient(URI)
db = client[cfg.MONGO.DB]


def main(stock_pool=None, start_dt=None, collection_name=None):
    collection_name = collection_name or 'algo_00'
    _c = db[collection_name]
    print(f"@@@ USE MONGO#  DB:[{cfg.MONGO.DB}]  COLLECTION: [{collection_name}]")
    start_time = datetime.datetime.now()
    print(f"⏳ 程序启动时间: {start_time}")
    # 设置tushare pro的token并获取连接
    ts.set_token(cfg.BASE.TUSHARE_TOKEN)
    pro = ts.pro_api()
    # 设定获取日线行情的初始日期和终止日期，其中终止日期设定为昨天。
    start_dt = '20200101' if start_dt is None else start_dt.replace('-', '')
    print(f"## 抓取起始日期: {start_dt}")

    end_dt = datetime.datetime.now().strftime('%Y%m%d')

    # 设定需要获取数据的股票池
    stock_pool = cfg.STOCK.HS300 if stock_pool is None else stock_pool
    total = len(stock_pool)
    print(f"## 准备抓取 {total} 支股票数据...")

    # 查询当前数据行数
    count = _c.count_documents({})
    print(f"更新前数据条数: {count}")

    # 清空数据表
    _c.delete_many({})

    count = _c.count_documents({})
    print(f"清空后数据条数: {count}")

    # 循环获取单个股票的日线行情
    for i in range(len(stock_pool)):
        try:
            df = pro.daily(ts_code=stock_pool[i], start_date=start_dt, end_date=end_dt)
            print('Seq: ' + str(i + 1) + ' of ' + str(total) + '   Code: ' + str(stock_pool[i]))
            c_len = df.shape[0]
        except Exception as aa:
            print(aa)
            # send_dingding_error_msg(aa)
            print('No DATA Code: ' + str(i))
            continue
        for j in range(c_len):
            resu0 = list(df.iloc[c_len - 1 - j])
            resu = []
            for k in range(len(resu0)):
                if str(resu0[k]) == 'nan':
                    resu.append(-1)
                else:
                    resu.append(resu0[k])
            state_dt = (datetime.datetime.strptime(resu[1], "%Y%m%d")).strftime('%Y-%m-%d')
            try:
                data = {
                    'state_dt': state_dt,
                    'stock_code': str(resu[0]),
                    'open': float(resu[2]),
                    'close': float(resu[5]),
                    'high': float(resu[3]),
                    'low': float(resu[4]),
                    'vol': float(resu[9]),
                    'amount': float(resu[10]),
                    'pre_close': float(resu[6]),
                    'amt_change': float(resu[7]),
                    'pct_change': float(resu[8])
                }
                _c.insert_one(data)
            except Exception:
                continue
        time.sleep(cfg.BASE.TUSHARE_SLEEP)

    # 查询更新后的数据行数
    count = _c.count_documents({})
    print(f"💰 新入库数据条数: {count}")

    end_time = datetime.datetime.now()
    print(f"⌛️ 程序结束时间: {end_time}")
    time_cost = end_time - start_time
    print(f"⌛️ 总耗时: {time_cost}")

    print('🎉🎉🎉 Init MONGO Finished!')


if __name__ == '__main__':
    # print(cfg.STOCK.HS300)
    main(cfg.STOCK.HSZZ, start_dt='2020-11-11')
