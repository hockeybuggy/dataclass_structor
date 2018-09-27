import decimal
import datetime
import enum
import uuid
from typing import Any, List, Optional, Set, Tuple, Type, TypeVar, Union


T = TypeVar("T")


def structure(value: Any, goal_type: Any) -> Any:
    """Returns object given a value and type signature to be coerced into.

    :param value: A dict or list composed of primitive type (str, int, float)
        or a primitive type.
    :param goal_type: A type that you would like cast `value` into.

    Usage::

      >>> import datetime
      >>> import dataclass_structor
      >>> dataclass_structor.structure('2018-10-02', datetime.date)
      datetime.datetime(2018, 10, 2)
    """
    if value is None:
        return value
    if hasattr(goal_type, "__origin__") and goal_type.__origin__ is Union:
        return _structure_union(value, goal_type.__args__)
    return _structure_value(value, goal_type)


_structure_value_condition_conversion_pairs = [
    (lambda v, gt: isinstance(v, dict), lambda v, gt: _try_structure_object(v, gt)),
    (
        lambda v, gt: hasattr(gt, "_name") and gt._name == "Tuple",
        lambda v, gt: _try_structure_tuple(v, gt),
    ),
    (
        lambda v, gt: hasattr(gt, "_name") and gt._name == "Set",
        lambda v, gt: _try_structure_set(v, gt),
    ),
    (lambda v, gt: isinstance(v, list), lambda v, gt: _try_structure_list(v, gt)),
    (lambda v, gt: isinstance(v, float), lambda v, gt: _try_structure_float(v, gt)),
    (lambda v, gt: isinstance(v, int), lambda v, gt: _try_structure_int(v, gt)),
    (lambda v, gt: isinstance(v, str), lambda v, gt: _try_structure_str(v, gt)),
]


def _structure_value(value: Any, goal_type: Type[T]) -> T:
    for condition, conversion in _structure_value_condition_conversion_pairs:
        if condition(value, goal_type):
            # This could be a good place for PEP 572 the assignment operator
            # but since Python 3.7 is a target we shall do without.
            obj = conversion(value, goal_type)
            if obj is not None:
                return obj
    raise ValueError(
        f"Could not structure: {value} of type {type(value)} into {goal_type}"
    )


_structure_union_type_priority = (
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


def _structure_union(value: Any, union_types: Tuple[Type[T]]) -> Optional[T]:
    results = {}
    for a_type in union_types:
        try:
            results[a_type] = structure(value, a_type)
        except ValueError:
            pass

    for a_type in _structure_union_type_priority:
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


def _try_convert_string_to_decimal(value):
    try:
        return decimal.Decimal(value)
    except decimal.InvalidOperation as ex:
        raise ValueError from ex


_structure_str_goal_type_to_conversion_map = {
    int: lambda v: int(v),
    float: lambda v: float(v),
    decimal.Decimal: lambda v: _try_convert_string_to_decimal(v),
    datetime.datetime: lambda v: datetime.datetime.fromisoformat(v),
    datetime.date: lambda v: datetime.date.fromisoformat(v),
    uuid.UUID: lambda v: uuid.UUID(v),
}


def _try_structure_str(value: str, goal_type: Any) -> Any:
    conversion = _structure_str_goal_type_to_conversion_map.get(goal_type)
    if conversion:
        try:
            return conversion(value)
        except ValueError as ex:
            raise ValueError(
                f"Could not convert {value} of type {type(value)} into a {goal_type}."
            ) from ex

    if hasattr(goal_type, "mro") and enum.Enum in goal_type.mro():
        if value in goal_type.__members__:
            return goal_type[value]
        try:
            return getattr(str, goal_type)
        except TypeError as ex:
            raise ValueError(
                f"Could not convert {value} of type {type(value)} into a {goal_type} enum."
            ) from ex
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


def _try_structure_tuple(value: Tuple[Any], goal_type: Any) -> Tuple:
    tuple_content_types = goal_type.__args__
    return tuple(structure(value[i], t) for i, t in enumerate(tuple_content_types))
