from bnp.algo.algo_01 import init_db, search_target  # noqa
from bnp.settings import cfg  # noqa
from bnp.utils import send_dingding_msg, today_str
from pymongo import MongoClient

URI = f"mongodb://{cfg.MONGO.USERNAME}:{cfg.MONGO.PASSWORD}@{cfg.MONGO.HOST}:{cfg.MONGO.PORT}/{cfg.MONGO.DB}?authMechanism=SCRAM-SHA-1"  # noqa
client = MongoClient(URI)
db = client[cfg.MONGO.DB]

L = []
res = ['000001.SZ', '000069.SZ']
for ts_code in res:
    item = db.stock_info.find_one({'ts_code': ts_code})
    print(item['ts_code'], item['name'], item['industry'], item['market'])
    L.append({'ts_code': item['ts_code'], 'name': item['name'], 'industry': item['industry'], 'market': item['market']})

msg = {
    'date': today_str(),
    'stocks': L
}
send_dingding_msg(msg)
