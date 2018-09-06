
# Python Data class serializer/deserializer


## Install

```shell
pip install data_structor
```

## Usage

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
