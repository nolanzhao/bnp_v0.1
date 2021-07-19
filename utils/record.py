from bnp.settings import cfg
from bnp.utils import today_str
from pymongo import MongoClient

URI = f"mongodb://{cfg.MONGO.USERNAME}:{cfg.MONGO.PASSWORD}@{cfg.MONGO.HOST}:{cfg.MONGO.PORT}/{cfg.MONGO.DB}?authMechanism=SCRAM-SHA-1"  # noqa
client = MongoClient(URI)
db = client[cfg.MONGO.DB]


def save_record(stocks, algo=None):
    if stocks is None or algo is None:
        return
    db.record.delete_many({'date': today_str(), 'algo': algo})
    db.record.insert_one({'date': today_str(), 'algo': algo, 'stocks': stocks})
