import decimal
import datetime
import enum
import uuid
from dataclasses import fields, is_dataclass
from typing import Any


def unstructure(value: Any) -> Any:
    """Returns dictionary given a value of a particular type"""
    if value is None:
        return value
    if isinstance(value, str):
        return value
    if isinstance(value, float):
        return value
    if isinstance(value, int):
        return value
    if isinstance(value, decimal.Decimal):
        return str(value)
    if isinstance(value, uuid.UUID):
        return str(value)
    if isinstance(value, enum.Enum):
        return value.name
    if isinstance(value, datetime.datetime) or isinstance(value, datetime.date):
        return value.isoformat()
    if isinstance(value, list):
        return [unstructure(v) for v in value]
    if isinstance(value, set):
        return set([unstructure(v) for v in value])
    if isinstance(value, dict):
        return {k: unstructure(v) for k, v in value.items()}
    if is_dataclass(value):
        return {f.name: unstructure(getattr(value, f.name)) for f in fields(value)}
    raise ValueError(f"Could not unstructure: {value}")
