import json

import requests
from bnp.settings import cfg


def send_dingding_msg(msg, api=cfg.DINGDING.API, title=cfg.DINGDING.TITLE):
    info = f"{msg['date']}\n\n"
    if len(msg['stocks']) == 0:
        info += f"🐶🐶🐶 [{msg['algo']}]\n"
    else:
        info += f"🎉🎉🎉 [{msg['algo']}]\n"
        for stock in msg['stocks']:
            if 'algo' in stock:
                info += f"\n> {stock['algo']}"
                info += f"\n> {stock['ts_code']} {stock['name']} {stock['industry']} {stock['market']}"
                info += "\n"
            else:
                info += f"\n> {stock['ts_code']} {stock['name']} {stock['industry']} {stock['market']}"

    data = {"msgtype": "markdown", "markdown": {"title": "车票速递", "text": info}}
    print(data)
    headers = {'Content-Type': 'application/json;charset=utf-8'}
    requests.post(api, json.dumps(data), headers=headers)


def send_dingding_error_msg(msg, api=cfg.DINGDING.API, title=cfg.DINGDING.TITLE):
    info = "👾👾👾\n\n"
    info += msg

    data = {"msgtype": "markdown", "markdown": {"title": "报错信息", "text": info}}
    print(data)
    headers = {'Content-Type': 'application/json;charset=utf-8'}
    requests.post(api, json.dumps(data), headers=headers)
