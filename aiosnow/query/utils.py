from typing import Union

from aiosnow.exceptions import SelectError

from .condition import Condition
from .selector import Selector


def select(value: Union[Selector, Condition, str] = None) -> Selector:
    if value is None or isinstance(value, str):
        sysparms = value or ""
    elif isinstance(value, Condition):
        sysparms = value.serialize_registry()
    elif isinstance(value, Selector):
        return value
    else:
        raise SelectError(f"Can only query by type {Condition} or {str}")

    return Selector(sysparms)
