import datetime
import decimal
import enum
import uuid

import pytest

from dataclass_structor import structure


def test_structure__bad_str__int():
    with pytest.raises(ValueError) as exinfo:
        structure("Tomato", int)
    assert "Could not convert Tomato of type <class 'str'> into an int" in str(
        exinfo.value
    )


def test_structure__bad_str__float():
    with pytest.raises(ValueError) as exinfo:
        structure("Tomato", float)
    assert "Could not convert Tomato of type <class 'str'> into a float" in str(
        exinfo.value
    )


def test_structure__bad_str__decimal():
    with pytest.raises(ValueError) as exinfo:
        structure("Tomato", decimal.Decimal)
    assert (
        "Could not convert Tomato of type <class 'str'> into a decimal.Decimal"
        in str(exinfo.value)
    )


def test_structure__bad_str__date():
    with pytest.raises(ValueError) as exinfo:
        structure("Tomato", datetime.date)
    assert "Could not convert Tomato of type <class 'str'> into a datetime.date" in str(
        exinfo.value
    )


def test_structure__bad_str__datetime():
    with pytest.raises(ValueError) as exinfo:
        structure("Tomato", datetime.datetime)
    assert (
        "Could not convert Tomato of type <class 'str'> into a datetime.datetime"
        in str(exinfo.value)
    )


def test_structure__bad_str__uuid():
    with pytest.raises(ValueError) as exinfo:
        structure("Tomato", uuid.UUID)
    assert "Could not convert Tomato of type <class 'str'> into a uuid.UUID" in str(
        exinfo.value
    )


def test_structure__bad_str__int_enum():
    class Animal(enum.Enum):
        ANT = 1
        BEE = 2
        CAT = 3
        DOG = 4

    with pytest.raises(ValueError) as exinfo:
        structure("Tomato", Animal)
    assert (
        "Could not convert Tomato of type <class 'str'> into a <enum 'Animal'> enum."
        in str(exinfo.value)
    )


def test_structure__bad_str__str_enum():
    class Sounds(enum.Enum):
        CAT = "meow"
        DOG = "dog"

    with pytest.raises(ValueError) as exinfo:
        structure("Tomato", Sounds)
    assert (
        "Could not convert Tomato of type <class 'str'> into a <enum 'Sounds'> enum."
        in str(exinfo.value)
    )
