import datetime
import time

import pymysql
import tushare as ts
from bnp.settings import cfg


def main(stock_pool=None, start_dt=None):
    start_time = datetime.datetime.now()
    print(f"⏳ 程序启动时间: {start_time}")
    # 设置tushare pro的token并获取连接
    ts.set_token(cfg.BASE.TUSHARE_TOKEN)
    pro = ts.pro_api()
    # 设定获取日线行情的初始日期和终止日期，其中终止日期设定为昨天。
    start_dt = '20200101' if start_dt is None else start_dt.replace('-', '')
    print(f"## 抓取起始日期: {start_dt}")

    end_dt = datetime.datetime.now().strftime('%Y%m%d')

    # 建立数据库连接,剔除已入库的部分
    db = pymysql.connect(host=cfg.MYSQL.HOST,
                         user=cfg.MYSQL.USER,
                         passwd=cfg.MYSQL.PASSWD,
                         db=cfg.MYSQL.DB,
                         charset=cfg.MYSQL.CHARSET)
    cursor = db.cursor()
    # 设定需要获取数据的股票池
    stock_pool = cfg.STOCK.HS300 if stock_pool is None else stock_pool
    total = len(stock_pool)
    print(f"## 准备抓取 {total} 支股票数据...")

    # 查询当前数据行数
    sql_count = "SELECT COUNT(*) FROM stock_all_test"
    cursor.execute(sql_count)
    res = cursor.fetchone()
    print(f"更新前数据条数: {res[0]}")

    # 清空数据表
    sql_count = "truncate table stock_all_test"
    cursor.execute(sql_count)

    sql_count = "SELECT COUNT(*) FROM stock_all_test"
    cursor.execute(sql_count)
    res = cursor.fetchone()
    print(f"清空后数据条数: {res[0]}")

    # 循环获取单个股票的日线行情
    for i in range(len(stock_pool)):
        try:
            df = pro.daily(ts_code=stock_pool[i], start_date=start_dt, end_date=end_dt)
            print('Seq: ' + str(i + 1) + ' of ' + str(total) + '   Code: ' + str(stock_pool[i]))
            c_len = df.shape[0]
        except Exception as aa:
            print(aa)
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
                sql_insert = "INSERT INTO stock_all_test(state_dt,stock_code,open,close,high,low,vol,amount,pre_close,amt_change,\
                    pct_change) VALUES ('%s', '%s', '%.2f', '%.2f','%.2f','%.2f','%i','%.2f','%.2f','%.2f','%.2f')" % (
                    state_dt, str(resu[0]), float(resu[2]), float(resu[5]), float(resu[3]), float(resu[4]), float(
                        resu[9]), float(resu[10]), float(resu[6]), float(resu[7]), float(resu[8]))
                cursor.execute(sql_insert)
                db.commit()
            except Exception:
                continue
        time.sleep(0.2)

    # 查询更新后的数据行数
    cursor.execute(sql_count)
    res = cursor.fetchone()
    print(f"💰 新入库数据条数: {res[0]}")

    cursor.close()
    db.close()

    end_time = datetime.datetime.now()
    print(f"⌛️ 程序结束时间: {end_time}")
    time_cost = end_time - start_time
    print(f"⌛️ 总耗时: {time_cost}")

    print(f'🎉🎉🎉 Init MYSQL TEST DATA Finished!  ({start_dt} ~ today)')


if __name__ == '__main__':
    # print(cfg.STOCK.HS300)
    main(cfg.STOCK.ZZ500, start_dt='2018-01-01')
