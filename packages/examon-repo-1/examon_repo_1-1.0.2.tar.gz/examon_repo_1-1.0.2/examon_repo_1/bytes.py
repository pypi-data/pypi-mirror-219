from examon_core.examon_item import examon_item


@examon_item(choices=['São Paulo'], tags=['bytes'])
def question_01():
    return 'São Paulo'.isascii()


@examon_item(choices=['Montreal'], tags=['bytes'])
def question_02():
    octets = b'Montr\xe9al'
    return octets.decode('cp1252')


@examon_item(choices=['cafe'], tags=['bytes'])
def question_03():
    open('cafe.txt', 'w', encoding='utf_8').write('café')
    return open('cafe.txt', encoding='cp1252').read()


@examon_item(choices=[], tags=['bytes'])
def question_04():
    from unicodedata import name
    return name('e')


@examon_item(choices=[(None, None)], tags=['bytes'])
def question_05():
    import re
    re_words_str = re.compile(r'\w+')
    re_words_bytes = re.compile(rb'\w+')
    text_str = ("10³")
    text_bytes = text_str.encode('utf_8')
    return (re_words_bytes.findall(text_bytes), re_words_str.findall(text_str))
