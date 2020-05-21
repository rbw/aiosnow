from typing import Any, Tuple, Union

import marshmallow

from .numeric import Numeric
from .text import Text


class TextMapping:
    def __init__(self, id_value: str, text_value: str):
        self.id = id_value
        self.text = text_value


class NumericMapping:
    def __init__(self, id_value: int, text_value: str):
        self.id = id_value
        self.text = text_value


class MappedField(marshmallow.fields.Tuple):
    @property
    def _tuple_fields(self) -> Tuple[Union[Numeric, Text], Text]:
        raise NotImplementedError

    def __init__(self, *args: Any, **kwargs: Any):
        super(MappedField, self).__init__(self._tuple_fields, *args, **kwargs)


class NumericMap(MappedField, Numeric):
    def _deserialize(self, *args: Any, **kwargs: Any) -> Any:
        result = super()._deserialize(*args, **kwargs)
        return NumericMapping(*result)

    def _serialize(self, *args: Any, **kwargs: Any) -> Any:
        return super()._serialize(*args, **kwargs)

    _tuple_fields = Numeric(), Text()


class TextMap(MappedField, Text):
    def _deserialize(self, *args: Any, **kwargs: Any) -> Any:
        result = super()._deserialize(*args, **kwargs)
        return TextMapping(*result)

    def _serialize(self, *args: Any, **kwargs: Any) -> Any:
        return super()._serialize(*args, **kwargs)

    _tuple_fields = Text(), Text()
