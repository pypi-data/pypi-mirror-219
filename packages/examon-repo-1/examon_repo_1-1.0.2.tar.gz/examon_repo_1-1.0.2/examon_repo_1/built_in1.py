from examon_core.examon_item import examon_item


@examon_item(choices=['São Paulo'], tags=['seed'])
def question_01():
    import random

    random.seed(10)
    return random.random() == random.random()
