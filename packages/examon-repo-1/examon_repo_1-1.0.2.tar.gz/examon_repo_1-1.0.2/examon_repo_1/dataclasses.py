from examon_core.examon_item import examon_item


@examon_item(choices=['wrong answer'], tags=['mytag'])
def question_01():
    class Coordinate:
        def __init__(self, lat, lon):
            self.lat = lat
            self.lon = lon

    return Coordinate(55.76, 37.62) == Coordinate(55.76, 37.62)


@examon_item(choices=[], tags=['dataclasses'])
def question_02():
    from collections import namedtuple
    Coordinate = namedtuple('Coordinate', 'lat lon')
    return Coordinate(
        lat=55.756,
        lon=37.617) == Coordinate(
        lat=55.756,
        lon=37.617)


@examon_item(choices=[], tags=['dataclasses'])
def question_03():
    import typing
    Coordinate = typing.NamedTuple(
        'Coordinate', [
            ('lat', float), ('lon', float)])
    return typing.get_type_hints(Coordinate)


@examon_item(choices=[], tags=['dataclasses'])
def question_04():
    from collections import namedtuple
    import typing
    CoordinateA = namedtuple('Coordinate', 'lat lon')
    CoordinateB = typing.NamedTuple(
        'Coordinate', [('lat', float), ('lon', float)])
    return CoordinateB(
        lat=55.756,
        lon=37.617) == CoordinateA(
        lat=55.756,
        lon=37.617)



@examon_item(choices=[], tags=['dataclasses'])
def question_06():
    from typing import NamedTuple

    class Word(NamedTuple):
        word: string

    return (issubclass(Word, typing.NamedTuple), issubclass(Word, tuple))


@examon_item(choices=[], tags=['dataclasses'])
def question_07():
    from dataclasses import dataclass

    @dataclass(frozen=True)
    class Word:
        word: string

    return Word('Hello').asdict()


@examon_item(choices=[], tags=['dataclasses'])
def question_08():
    from collections import namedtuple
    City = namedtuple('City', 'name country population coordinates')
    return City._fields


@examon_item(choices=[], tags=['dataclasses'])
def question_09():
    from collections import namedtuple
    City = namedtuple('City', 'name country population')
    delhi = City._make(('Delhi NCR', 'IN', 21.935))
    return delhi._asdict()


@examon_item(choices=[], tags=['dataclasses'])
def question_10():
    from collections import namedtuple
    City = namedtuple('City', 'name country population')

    def desc_function(city):
        return f'{city.name}, {city.country}, {city.population}'

    City.desc = desc_function

    return City('Delhi NCR', 'IN', 21.935).desc()


@examon_item(choices=[], tags=['dataclasses'])
def question_11():
    from typing import NamedTuple

    class Coordinate(NamedTuple):
        lat: float
        lon: float
        reference: str = 'WGS84'

    coord = Coordinate('Ni!', None)
    return coord


@examon_item(choices=[], tags=['dataclasses'])
def question_12():
    class DemoPlainClass:
        a: int
        b: float = 1.1
        c = 'spam'

    return DemoPlainClass.__annotations__


@examon_item(choices=[], tags=['dataclasses'])
def question_13():
    class DemoPlainClass:
        a: int
        b: float = 1.1
        c = 'spam'

    return DemoPlainClass.a


@examon_item(choices=[], tags=['dataclasses'])
def question_14():
    class DemoPlainClass:
        a: int
        b: float = 1.1
        c = 'spam'

    return (DemoPlainClass.b, DemoPlainClass.c)


@examon_item(choices=[], tags=['dataclasses'])
def question_15():
    import typing

    class DemoNTClass(typing.NamedTuple):
        a: int
        b: float = 1.1
        c = 'spam'

    nt = DemoNTClass(8)
    return (nt.a, nt, b, bt.c)


@examon_item(choices=[], tags=['dataclasses'])
def question_16():
    from dataclasses import dataclass
    import typing

    class DemoNTClass(typing.NamedTuple):
        a: int
        b: float = 1.1
        c = 'spam'

    @dataclass
    class DemoDataClass:
        a: int
        b: float = 1.1
        c = 'spam'

    return DemoDataClass.__annotations__ == DemoNTClass.__annotations__


@examon_item(choices=[], tags=['dataclasses'])
def question_17():
    from dataclasses import dataclass
    import typing

    class DemoNTClass(typing.NamedTuple):
        a: int
        b: float = 1.1
        c = 'spam'

    @dataclass
    class DemoDataClass:
        a: int
        b: float = 1.1
        c = 'spam'

    return (DemoDataClass(1).a, DemoNTClass(1).a)


@examon_item(choices=[], tags=['dataclasses'])
def question_18():
    from dataclasses import dataclass
    import typing

    class DemoNTClass(typing.NamedTuple):
        a: int
        b: float = 1.1
        c = 'spam'

    @dataclass
    class DemoDataClass:
        a: int
        b: float = 1.1
        c = 'spam'

    return (DemoDataClass(1).c, DemoNTClass(1).c)


@examon_item(choices=[], tags=['dataclasses'])
def question_19():
    from dataclasses import dataclass
    import typing

    @dataclass(init=False, repr=False, eq=False, order=False,
               unsafe_hash=False, frozen=False)
    class DataClassA:
        pass

    @dataclass(init=True, repr=True, eq=True, order=True,
               unsafe_hash=True, frozen=True)
    class DataClassB:
        pass

    return set(dir(DataClassA.__class__)) - set(dir(DataClassB.__class__))


@examon_item(choices=[], tags=['dataclasses'])
def question_20():
    from dataclasses import dataclass, field

    @dataclass
    class ClubMember:
        name: str
        guests: list = field(default_factory=list)

    a = ClubMember('a')
    b = ClubMember('b')
    return (a.guests is None, a.guests is b.guests, a.guests == b.guests)


@examon_item(choices=[], tags=['dataclasses'])
def question_21():
    from dataclasses import dataclass, field

    @dataclass
    class ClubMember:
        name: str
        guests: list = field(default_factory=lambda: [1, 2, 3])

    return ClubMember('Bob').guests


@examon_item(choices=[], tags=['dataclasses'])
def question_22():
    from dataclasses import dataclass, field

    @dataclass
    class Actor:
        name: str
        age: int
        cool: str = field(init=False, repr=False)

        def __post_init__(self):
            if self.name == 'Tom Cruise':
                self.age = 35

    return (Actor('Tom Cruise', 60).age, Actor('Val Kilmer', 60).age)


@examon_item(choices=[], tags=['dataclasses'])
def question_23():
    from dataclasses import dataclass, field, InitVar

    @dataclass
    class Actor:
        name: str
        age: int = field(repr=False)
        bio: InitVar[str] = None

    def __post_init__(self):
        if self.bio == 'Tom Cruise':
            print(self.bio)

    a = Actor('Tom Cruise', 60, bio='somethign')
    return str(a)
