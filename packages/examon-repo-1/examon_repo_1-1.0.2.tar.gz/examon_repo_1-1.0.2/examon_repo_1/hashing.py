from examon_core.examon_item import examon_item

@examon_item(choices=[], tags=['built in functions'])
def question_01():
    return type(hash((10, 'alpha', (1, 2))))


def question_02():
    return type(hash((10, 'alpha', [1, 2])))

@examon_item(choices=[], tags=['sets'])
def question_04():
    x = {"apple", "banana", "cherry"}
    try:
        hash(x)
    except Exception:
        return 'error'
    return 'ok'


@examon_item(choices=[], tags=['sets'])
def question_05():
    x = frozenset(["apple", "banana", "cherry"])
    try:
        hash(x)
    except Exception:
        return 'error'
    return 'ok'