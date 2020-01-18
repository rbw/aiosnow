from snow.exceptions import SelectError

from .builder import QueryBuilder
from .segment import Segment


def select(value=None):
    if value is None or isinstance(value, str):
        return QueryBuilder.from_raw(value or "")
    elif isinstance(value, QueryBuilder):
        return value
    elif isinstance(value, Segment):
        return QueryBuilder.from_segments(value.instances)
    else:
        raise SelectError(f"Can only query by type {Segment} or {str}")
