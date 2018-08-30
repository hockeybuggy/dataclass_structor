from dataclasses import fields, is_dataclass
from typing import Any, Dict, Optional, Type, TypeVar


T = TypeVar("T")



def unstructure(value: Any) -> Dict[str, Any]:
    """Returns dictionary given a value of a particular type"""
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        return {k: unstructure(v) for k, v in value.items()}
    if is_dataclass(value):
        return {
            f.name: unstructure(getattr(value, f.name)) for f in fields(value)
        }
    raise ValueError(f"Could not destructure: {value}")


def structure(value: Any, goal_type: Type[T]) -> T:
    """Returns object given a value and type signature to be coerced into"""
    if isinstance(value, dict):
        obj = _try_structure_object(value, goal_type)
        if obj:
            return obj
    if isinstance(value, str):
        return value
    return value


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
