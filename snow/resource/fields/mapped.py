from collections import namedtuple
from typing import Tuple, Union

import marshmallow

from .text import Text
from .numeric import Numeric

Mapping = namedtuple("Mapping", ["id", "text"])


class MappedField(marshmallow.fields.Tuple):
    def _deserialize(self, *args, **kwargs) -> Tuple:
        result = super()._deserialize(*args, **kwargs)
        return Mapping(*result)

    @property
    def _tuple_fields(self) -> Tuple[Union[str, int], str]:
        raise NotImplementedError

    def __init__(self, *args, **kwargs):
        super(MappedField, self).__init__(self._tuple_fields, *args, **kwargs)


class NumericMap(MappedField, Numeric):
    _tuple_fields = Numeric(), Text()


class TextMap(MappedField, Text):
    _tuple_fields = Text(), Text()
