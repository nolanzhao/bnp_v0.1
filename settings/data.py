import os


def get_stock_codes(POOL='ZZ500'):
    res = []
    DATA_PATH = os.path.join(os.path.dirname(__file__), POOL)
    with open(DATA_PATH, 'r') as f:
        for line in f.readlines():
            code = line.split()[0]
            # print(code)
            if not code:
                continue
            res.append(code)
    return res


def get_subscriber():
    res = []
    DATA_PATH = os.path.join(os.path.dirname(__file__), 'SUBSCRIBER')
    with open(DATA_PATH, 'r') as f:
        for line in f.readlines():
            email_addr = line.split()[0]
            # print(email_addr)
            if not email_addr:
                continue
            res.append(email_addr)
    return res


if __name__ == '__main__':
    # print(get_stock_codes(POOL='HS300'))
    print(get_subscriber())
