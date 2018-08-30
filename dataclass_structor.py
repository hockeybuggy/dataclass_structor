import decimal
import datetime
import enum
import uuid
from dataclasses import fields, is_dataclass
from typing import Any, Dict, Optional, Type, TypeVar


T = TypeVar("T")


def unstructure(value: Any) -> Dict[str, Any]:
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
    if isinstance(value, dict):
        return {k: unstructure(v) for k, v in value.items()}
    if is_dataclass(value):
        return {
            f.name: unstructure(getattr(value, f.name)) for f in fields(value)
        }
    raise ValueError(f"Could not unstructure: {value}")


def structure(value: Any, goal_type: Type[T]) -> T:
    """Returns object given a value and type signature to be coerced into"""
    if isinstance(value, dict):
        obj = _try_structure_object(value, goal_type)
        if obj:
            return obj
    if isinstance(value, str) and goal_type == float:
        return float(value)
    if isinstance(value, str) and goal_type == decimal.Decimal:
        return decimal.Decimal(value)

    if isinstance(value, str) and goal_type == datetime.datetime:
        return datetime.datetime.fromisoformat(value)
    if isinstance(value, str) and goal_type == datetime.date:
        return datetime.date.fromisoformat(value)
    if isinstance(value, str) and goal_type == uuid.UUID:
        return uuid.UUID(value)
    if isinstance(value, str) and hasattr(goal_type, "mro") and enum.Enum in goal_type.mro():
        if value in goal_type.__members__:
            return goal_type[value]
        return getattr(str, goal_type)
    if isinstance(value, str):
        return value

    if isinstance(value, int) and goal_type == decimal.Decimal:
        return decimal.Decimal(value)
    if isinstance(value, int):
        return value

    if isinstance(value, float) and goal_type == decimal.Decimal:
        return decimal.Decimal(value)
    if isinstance(value, float) and goal_type == float:
        return value

    if value is None:
        return value
    raise ValueError(f"Could not structure: {value} into {goal_type}")


# TODO this could have a better type for value
def _try_structure_object(value: Any, goal_type: Type[T]) -> Optional[T]:
    try:
        return goal_type(
            **{
                k: structure(v, type(v))
                for k, v in value.items()
            }
        )
    except (KeyError, ValueError):
        pass
    if issubclass(goal_type, dict):
        dict_value_type = goal_type.__args__[1]  # type: ignore
        return {
            k: structure(v, dict_value_type)
            for k, v in value.items()
        }
    return None
