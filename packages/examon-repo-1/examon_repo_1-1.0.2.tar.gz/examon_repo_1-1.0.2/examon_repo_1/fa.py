from examon_core.examon_item import examon_item


@examon_item(choices=[1, 2, 3, 4, 5, 6, 7], tags=['fa'])
def question_01():
    def a(array):
        return array[1]

    return a([1, 2, 3, 4, 5, 6, 7])


@examon_item(choices=[1, 2, 3, 4, 5, 6, 7], tags=['fa'])
def question_01():
    def a(array):
        sorted(array)
        return array[-1]

    return a([1, 2, 3, 4, 5, 6, 7])


@examon_item(choices=[1, 2, 3, 4, 5, 6, 7], tags=['fa'])
def question_01():
    def a(array):
        return [a for a in array]

    return a([1, 2, 3, 4, 5, 6, 7])


@examon_item(choices=[1, 2, 3, 4, 5, 6, 7], tags=['fa'])
def question_01():
    def a(array):
        return [a for a in array if isinstance(a, int)]

    return a([1, 2, 3, '4', 5, 6, 7, None])[2]

@examon_item(choices=[1, 2, 3, 4, 5, 6, 7], tags=['fa'])
def question_01():
    def filter(array):
        return [a for a in array if isinstance(a, int)]

    a = filter([1, 2, 3, '4', 5, 6, 7, None])
    sorted(a)
    return a[-2]

@examon_item(choices=[1, 2, 3, 4, 5, 6, 7], tags=['fa'])
def question_01():
    def my_filter(array):
        return [a for a in array if isinstance(a, int)]

    def my_sort(a):
        sorted(a)

    a = my_filter([1, 2, 3, '4', 5, 6, 7, None])
    my_sort(a)
    return a[-3]