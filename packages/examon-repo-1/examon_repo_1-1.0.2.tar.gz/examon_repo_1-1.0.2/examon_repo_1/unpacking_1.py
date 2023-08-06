from examon_core.examon_item import examon_item



@examon_item(choices=[], tags=['unpacking', 'easy'])
def question_01():
    lax_coordinates = (33.9425, -118.408056)
    latitude, longitude = lax_coordinates
    return latitude


@examon_item(choices=[], tags=['unpacking', 'easy'])
def question_02():
    *rest, a, b = range(5)
    return rest[1]


@examon_item(choices=[], tags=['unpacking', 'easy'])
def question_03():
    a, *rest, b = range(5)
    return rest[1]


@examon_item(choices=[], tags=['unpacking', 'moderate'])
def question_04():
    def fun(a, b, c, d, *rest):
        return a, b, c, d, rest

    return fun(*[1, 2], 3, *range(4, 7))[3]


@examon_item(choices=[], tags=['unpacking', 'easy'])
def question_05():
    a, b, *rest = range(5)
    return b


@examon_item(choices=[], tags=['unpacking', 'hard'])
def question_06():
    def my_function(*args, **kwargs):
        return (args, kwargs)

    return my_function(1, 2, b=3, c=4)
