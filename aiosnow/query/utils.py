from typing import Union

from aiosnow.exceptions import SelectError

from .builder import QueryBuilder
from .condition import Condition


def select(value: Union[QueryBuilder, Condition, str] = None) -> QueryBuilder:
    if value is None or isinstance(value, str):
        return QueryBuilder.from_raw(value or "")
    elif isinstance(value, QueryBuilder):
        return value
    elif isinstance(value, Condition):
        return QueryBuilder.from_chain(value.selection)
    else:
        raise SelectError(f"Can only query by type {Condition} or {str}")
