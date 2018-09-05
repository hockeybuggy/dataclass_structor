import enum

from dataclass_structor import structure, unstructure


class Animal(enum.Enum):
    ANT = 1
    BEE = 2
    CAT = 3
    DOG = 4


def test_unstructure__animal():
    assert unstructure(Animal.ANT) == "ANT"


def test_structure__animal():
    assert structure("BEE", Animal) == Animal.BEE


class Sounds(enum.Enum):
    CAT = "meow"
    DOG = "dog"


def test_unstructure__sounds():
    assert unstructure(Sounds.CAT) == "CAT"


def test_structure__sounds():
    assert structure("DOG", Sounds) == Sounds.DOG
