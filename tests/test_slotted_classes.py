import typing

from dataclass_structor import structure, unstructure


class Guest:
    __slots__ = ("first_name",)

    def __init__(self, first_name: typing.Optional[str] = None):
        self.first_name = first_name

    def __repr__(self):
        return f"Guest(first_name={repr(self.first_name)})"

    def __eq__(self, other):
        return self.first_name == other.first_name


def test_unstructure__guest_with_first_name():
    expected = {"first_name": "Bobby Jim"}
    assert unstructure(Guest(first_name="Bobby Jim")) == expected


def test_structure__guest_with_first_name():
    expected = Guest(first_name="Bobby Jim")
    assert structure({"first_name": "Bobby Jim"}, Guest) == expected


def test_unstructure__guest_without_first_name():
    expected = {"first_name": None}
    assert unstructure(Guest(first_name=None)) == expected


def test_structure__guest_without_first_name():
    expected = Guest(first_name=None)
    assert structure({"first_name": None}, Guest) == expected
