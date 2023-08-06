from examon_core.examon_item import examon_item


@examon_item(choices=[3, 4, 'Exception'], tags=['assignment', 'very_easy'])
def question_01():
    A = 3
    A = 4
    return A


@examon_item(choices=[7, 4], tags=['assignment', 'very_easy'])
def question_02():
    a = 3
    a *= 4
    return a
