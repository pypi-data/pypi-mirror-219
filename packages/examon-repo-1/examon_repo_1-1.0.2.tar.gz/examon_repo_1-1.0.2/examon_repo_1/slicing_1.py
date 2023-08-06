from examon_core.examon_item import examon_item


@examon_item(choices=[], tags=['slicing', 'easy'])
def question_01():
    l = [10, 20, 30, 40, 50, 60]
    return l[2:]


@examon_item(choices=[], tags=['slicing', 'moderate'])
def question_02():
    l = [10, 20, 30, 40, 50, 60]
    return l[:2]


@examon_item(choices=[], tags=['slicing', 'moderate'])
def question_03():
    s = 'bicycle'
    return s[::3]


@examon_item(choices=[], tags=['slicing', 'moderate'])
def question_04():
    s = 'bicycle'
    return s[::1]

@examon_item(choices=[], tags=['slicing', 'moderate'])
def question_04():
    s = 'bicycle'
    return s[0::2]

@examon_item(choices=[], tags=['slicing', 'moderate'])
def question_05():
    l = list(range(10))
    l[2:5] = [20, 30]
    return l


@examon_item(choices=[], tags=['slicing', 'easy'])
def question_06():
    l = list(range(10))
    del l[5:7]
    return l


@examon_item(choices=[], tags=['slicing', 'hard'])
def question_07():
    l = list(range(10))
    l[3::2] = [11, 22]
    return l


@examon_item(choices=[], tags=['slicing', 'moderate'])
def question_07():
    class MySeq:
        def __getitem__(self, index):
            return index

    s = MySeq()
    return s[1:4:2, 9:10]


@examon_item(choices=[], tags=['slicing', 'moderate'])
def question_07():
    return 'ABCDE'[-3:] == 'ABCDE'[2:5:1]
