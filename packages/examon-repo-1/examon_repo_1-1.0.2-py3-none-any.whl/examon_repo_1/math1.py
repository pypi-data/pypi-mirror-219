from examon_core.examon_item import examon_item


from math import ceil, floor, trunc, factorial, hypot, sqrt


@examon_item(choices=[1,2,3,4,5], tags=['math'])
def question():
    return 1 + 3


@examon_item(choices=[1,2,3,4,5, 13], tags=['julian'])
def question():
    return 1 + 3 * 4

@examon_item(choices=[1,2,3,4,5], tags=['math'])
def question():
    from math import sqrt
    return sqrt(9)


@examon_item(choices=[1,2,3,4,5], tags=['math'])
def question():
    from math import floor
    return floor(9.6665456456)



@examon_item(choices=[1,2,3,4,5], tags=['math'])
def question():
    from math import ceil
    return ceil(9.6665456456)


@examon_item(choices=[], tags=['math'])
def question():
    from math import trunc
    return trunc(9.6665456456)


@examon_item(choices=[], tags=['math'])
def question():
    from math import hypot
    return hypot(5, 10)


@examon_item(choices=[], tags=['math'])
def question():
    from math import factorial
    return factorial(9)
