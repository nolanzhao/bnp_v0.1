from yacs.config import CfgNode as CN
from .data import get_stock_codes, get_subscriber

# BASE
BASE = CN()
BASE.TUSHARE_SLEEP = 0.5  # TUSHARE_API请求时SLEEP TIME
BASE.TUSHARE_TOKEN = ''  # 购买TUSHARE TOKEN（非广告, 非商业合作）

# MYSQL
MYSQL = CN()
MYSQL.HOST = ''
MYSQL.PORT = 3306
MYSQL.USER = ''
MYSQL.PASSWD = ''
MYSQL.DB = 'stock'  # 勿修改
MYSQL.CHARSET = 'utf8mb4'

# MONGO
MONGO = CN()

# MONGO.HOST = ''
# MONGO.PORT = 27017
# MONGO.USERNAME = ''
# MONGO.PASSWORD = ''
# MONGO.DB = 'fintech'  # 勿修改

MONGO.HOST = '127.0.0.1'
MONGO.PORT = 27017
MONGO.USERNAME = ''
MONGO.PASSWORD = ''
MONGO.DB = 'fintech'  # 勿修改

# STOCK
STOCK = CN()
STOCK.HS300 = get_stock_codes('HS300')
STOCK.ZZ500 = get_stock_codes('ZZ500')
STOCK.HSZZ = get_stock_codes('HSZZ')
STOCK.ZZ1K = get_stock_codes('ZZ1K')
STOCK.A3974 = get_stock_codes('A3974')
STOCK.C0925 = get_stock_codes('C0925')
STOCK.M2047 = get_stock_codes('M2047')
STOCK.MC2972 = get_stock_codes('MC2972')
STOCK.X1002 = get_stock_codes('X1002')
# STOCK.POOL = ['000100.SZ']

# MAIL
MAIL = CN()
MAIL.HOST = 'smtp.126.com'
MAIL.PORT = 465
MAIL.USER = ''
MAIL.PASS = ''
MAIL.SENDER = ''
MAIL.RECEIVERS = get_subscriber()
MAIL.FROM = MAIL.SENDER
MAIL.TO = '🤖 hello, frends.'
MAIL.SUBJECT = 'b.n.p'

# DINGDING
DINGDING = CN()
DINGDING.API = 'https://oapi.dingtalk.com/robot/send?access_token=xxxxxx'  # 请替换xxxxxx
DINGDING.TITLE = '今日代码'

# MAIN
_G = CN()
_G.BASE = BASE
_G.MYSQL = MYSQL
_G.MONGO = MONGO
_G.STOCK = STOCK
_G.MAIL = MAIL
_G.DINGDING = DINGDING


cfg = _G
