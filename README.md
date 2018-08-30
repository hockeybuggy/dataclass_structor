
# Python Data class serializer/deserializer



## Install

```shell
pipenv install 
```

## Usage

```python
import dataclasses

@dataclasses.dataclass
class Invite:
    email: str
    guests: typing.List["Guest"]

@dataclasses.dataclass
class Guest:
    first_name: typing.Optional[str] = None


x = to_dict(
  Invite(
    email="testing",
    guests=[
      Guest(first_name="John"),
      Guest(),
    ],
)
# x == {"email": "", "guests": [{"first_name": "John"}, {"first_name": None}]}
```


## Contributing

```shell
git clone <package>
pipenv install --dev
pipenv run pytest
```


## Questions to answer:

- Why not the dataclasses `asdict`?

- What about `cattrs`?

- What about `marshmallow`?

- Why is this not a JSON serializer?
