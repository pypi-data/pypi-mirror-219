def capasitor_parallel(c):
    res = 0
    for items in c:
        res += items
    return res

def capasitor_series(c):
    res = c.pop(0)
    while c:
        items = c.pop()
        res = (res*items)/(res+items)
    return res


def inductor_series(c):
    res = 0
    for items in c:
        res += items
    return res

def inductor_parallel(c):
    res = c.pop(0)
    while c:
        items = c.pop()
        res = (res*items)/(res+items)
    return res

def resistors_series(c):
    res = 0
    for items in c:
        res += items
    return res

def resistors_parallel(c):
    res = c.pop(0)
    while c:
        items = c.pop()
        res = (res*items)/(res+items)
    return res