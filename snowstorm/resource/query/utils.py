from snowstorm.exceptions import SelectError

from .builder import QueryBuilder
from .segment import Segment


def builder(value=""):
    if isinstance(value, QueryBuilder):
        return value
    elif isinstance(value, Segment):
        return QueryBuilder.from_segments(value.instances)
    elif isinstance(value, str):
        return QueryBuilder.from_raw(value)
    else:
        raise SelectError(f"Can only query by type {Segment} or {str}")
