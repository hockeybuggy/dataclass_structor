# data_structor

[![Build Status](https://travis-ci.com/hockeybuggy/dataclass_structor.svg?branch=master)](https://travis-ci.com/hockeybuggy/dataclass_structor)

[![Documentation Status](https://readthedocs.org/projects/dataclass-structor/badge/?version=latest)](https://dataclass-structor.readthedocs.io/en/latest/?badge=latest)


A type aware structor/destructor for python value objects.


## Install

```shell
pip install data_structor
```


## Documentation

The [docs for this project can be found here](dataclass-structor.readthedocs.io).


## Example

```python
import dataclasses

from data_structor import structure, unstructure


@dataclasses.dataclass
class Invite:
    email: str
    guests: typing.List["Guest"]


@dataclasses.dataclass
class Guest:
    first_name: typing.Optional[str] = None


value_type = Invite(
    email="testing",
    guests=[
      Guest(first_name="John"),
      Guest(),
    ],
)

x = unstructure(value_type)
assert x == {"email": "", "guests": [{"first_name": "John"}, {"first_name": None}]}

assert structure(x, Invite) == value_type
```
