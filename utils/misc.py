def cache(func):
    d = {}

    def deco(*args):
        # TODO: modify k
        k = f"{args[0]}-{args[1]}"
        if k in d:
            return d[k]
        res = func(*args)
        d[k] = res
        return res

    return deco
