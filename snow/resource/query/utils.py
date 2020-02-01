from snow.exceptions import SelectError

from .builder import QueryBuilder
from .condition import Condition


def select(value=None):
    if value is None or isinstance(value, str):
        return QueryBuilder.from_raw(value or "")
    elif isinstance(value, QueryBuilder):
        return value
    elif isinstance(value, Condition):
        return QueryBuilder.from_segments(value.instances)
    else:
        raise SelectError(f"Can only query by type {Condition} or {str}")
