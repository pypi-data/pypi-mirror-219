from examon_core.examon_item import examon_item


@examon_item(choices=[1, 2, 3, 4, 5, 6], tags=['itertools'])
def question():
    from itertools import accumulate
    GFG = [5, 3, 6, 2, 1, 9, 1]
    iter = accumulate(GFG, max)
    next(iter)
    next(iter)
    return next(iter)


@examon_item(choices=[1, 2, 3, 4, 5, 6], tags=['itertools'])
def question():
    from itertools import count
    iter = count(1, 3)
    next(iter)
    next(iter)
    return next(iter)


@examon_item(choices=[1, 2, 3, 4, 5, 6], tags=['itertools'])
def question():
    from itertools import groupby
    return [list(i[1]) for i in groupby('12216')]


@examon_item(choices=[1, 2, 3, 4, 5, 6], tags=['itertools'])
def question():
    from itertools import dropwhile
    return list(dropwhile(lambda x: x < 6, [1, 2, 2, 1, 6, 18, 9]))


@examon_item(choices=[True, False], tags=['itertools'])
def question():
    import itertools
    gen = itertools.takewhile(lambda n: n < 3, itertools.count(1, .5))
    return list(gen)

@examon_item(choices=[True, False], tags=['itertools'])
def question():
    import itertools
    def vowel(c):
        return c.lower() in 'aeiou'

    return list(itertools.filterfalse(vowel, 'Aardvark'))

@examon_item(choices=[True, False], tags=['itertools'])
def question():
    import itertools
    def vowel(c):
        return c.lower() in 'aeiou'

    return list(itertools.dropwhile(vowel, 'Aardvark'))

@examon_item(choices=[True, False], tags=['itertools'])
def question():
    import itertools
    def vowel(c):
        return c.lower() in 'aeiou'

    return list(itertools.takewhile(vowel, 'Aardvark'))

@examon_item(choices=[True, False], tags=['itertools'])
def question():
    import itertools

    return list(itertools.compress('Aardvark', (1, 0, 1, 1, 0, 1)))

@examon_item(choices=[True, False], tags=['itertools'])
def question():
    import itertools

    return list(itertools.islice('Aardvark', 4))

@examon_item(choices=[True, False], tags=['itertools'])
def question():
    import itertools

    return list(itertools.islice('Aardvark', 4, 7))

@examon_item(choices=[True, False], tags=['itertools'])
def question():
    import itertools

    return list(itertools.islice('Aardvark', 1, 7, 2))


@examon_item(choices=[True, False], tags=['itertools'])
def question():
    import itertools
    sample = [5, 4, 2, 8, 7, 6, 3, 0, 9, 1]
    return list(itertools.accumulate(sample))

@examon_item(choices=[True, False], tags=['itertools'])
def question():
    import itertools
    sample = [5, 4, 2, 8, 7, 6, 3, 0, 9, 1]
    return list(itertools.accumulate(sample, min))

@examon_item(choices=[True, False], tags=['itertools'])
def question():
    import itertools
    sample = [5, 4, 2, 8, 7, 6, 3, 0, 9, 1]
    return list(itertools.accumulate(sample, max))

@examon_item(choices=[True, False], tags=['itertools'])
def question():
    import itertools
    import operator
    sample = [5, 4, 2, 8, 7, 6, 3, 0, 9, 1]
    return list(itertools.accumulate(sample, operator.mul))

@examon_item(choices=[True, False], tags=['itertools'])
def question():
    import itertools
    return list(itertools.groupby('LLLLAAGGG'))