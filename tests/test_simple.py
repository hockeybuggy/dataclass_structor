import typing
import dataclasses

from dataclass_structor import structure, unstructure


@dataclasses.dataclass
class Invite:
    email: str
    guests: typing.List["Guest"]


@dataclasses.dataclass
class Guest:
    first_name: typing.Optional[str] = None


def test_guest__unstructure():
    expected = {"first_name": "Bobby Jim"}
    assert unstructure(Guest(first_name="Bobby Jim")) == expected


def test_guest__structure():
    expected = Guest(first_name="Bobby Jim")
    assert structure({"first_name": "Bobby Jim"}, Guest) == expected
