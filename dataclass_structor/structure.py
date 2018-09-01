import decimal
import datetime
import enum
import uuid
from typing import Any, List, Optional, Set, Tuple, Type, TypeVar, Union


T = TypeVar("T")


def structure(value: Any, goal_type: Any) -> Any:
    """Returns object given a value and type signature to be coerced into"""
    if value is None:
        return value
    if hasattr(goal_type, "__origin__") and goal_type.__origin__ is Union:
        return _structure_union(value, goal_type.__args__)
    return _structure_value(value, goal_type)


def _structure_value(value: Any, goal_type: Type[T]) -> T:
    if isinstance(value, dict):
        obj = _try_structure_object(value, goal_type)
        if obj:
            return obj
    if isinstance(value, list):
        obj = _try_structure_list(value, goal_type)
        if obj is not None:
            return obj
    if isinstance(value, set):
        obj = _try_structure_set(value, goal_type)
        if obj is not None:
            return obj
    if isinstance(value, float):
        obj = _try_structure_float(value, goal_type)
        if obj is not None:
            return obj
    if isinstance(value, int):
        obj = _try_structure_int(value, goal_type)
        if obj is not None:
            return obj
    if isinstance(value, str):
        obj = _try_structure_str(value, goal_type)
        if obj is not None:
            return obj
    raise ValueError(
        f"Could not structure: {value} of type {type(value)} into {goal_type}"
    )


def _structure_union(value: Any, union_types: Tuple[Type[T]]) -> Optional[T]:
    results = {}
    for a_type in union_types:
        try:
            results[a_type] = structure(value, a_type)
        except ValueError:
            pass
    type_priority = (
        datetime.datetime,
        datetime.date,
        uuid.UUID,
        dict,
        list,
        set,
        float,
        int,
        str,
    )
    for a_type in type_priority:
        if a_type in results:
            return results[a_type]
    return None


def _try_structure_object(value: Any, goal_type: Any) -> Any:
    try:
        return goal_type(**{k: structure(v, type(v)) for k, v in value.items()})
    except (KeyError, ValueError):
        pass
    if issubclass(goal_type, dict):
        dict_value_type = goal_type.__args__[1]
        return {k: structure(v, dict_value_type) for k, v in value.items()}
    return None


def _try_structure_str(value: str, goal_type: Any) -> Any:
    if goal_type == int:
        return int(value)
    if goal_type == float:
        return float(value)
    if goal_type == decimal.Decimal:
        return decimal.Decimal(value)
    if goal_type == datetime.datetime:
        return datetime.datetime.fromisoformat(value)
    if goal_type == datetime.date:
        return datetime.date.fromisoformat(value)  # type: ignore
    if goal_type == uuid.UUID:
        return uuid.UUID(value)
    if hasattr(goal_type, "mro") and enum.Enum in goal_type.mro():
        if value in goal_type.__members__:
            return goal_type[value]
        return getattr(str, goal_type)
    return value


def _try_structure_int(value: int, goal_type: Any) -> Union[int, decimal.Decimal, str]:
    if goal_type == decimal.Decimal:
        return decimal.Decimal(value)
    if goal_type == str:
        return str(value)
    return value


def _try_structure_float(
    value: float, goal_type: Any
) -> Union[float, decimal.Decimal, None]:
    if goal_type == decimal.Decimal:
        return decimal.Decimal(value)
    if goal_type == float:
        return value
    return None


def _try_structure_list(value: List[Any], goal_type: Any) -> List[Any]:
    list_content_type = goal_type.__args__[0]
    return [structure(v, list_content_type) for v in value]


def _try_structure_set(value: Set[Any], goal_type: Any) -> Set:
    set_content_type = goal_type.__args__[0]
    return set(structure(v, set_content_type) for v in value)
