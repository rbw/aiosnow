from abc import ABC
from typing import Any, Tuple, Union

import marshmallow

from .integer import Integer
from .string import String


class Mapping(ABC):
    id: Union[str, int, None] = None
    text: Union[str, None] = None

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} [id={self.id}, text={self.text}]>"


class StringMapping(Mapping):
    def __init__(self, id_value: str, text_value: str):
        self.id = id_value
        self.text = text_value


class IntegerMapping(Mapping):
    def __init__(self, id_value: int, text_value: str):
        self.id = id_value
        self.text = text_value


class MappedField(marshmallow.fields.Tuple):
    def __init__(self, *args: Any, **kwargs: Any):
        super(MappedField, self).__init__(self._tuple_fields, *args, **kwargs)

    @property
    def _tuple_fields(self) -> Tuple[Union[Integer, String], String]:
        raise NotImplementedError

    def _serialize(self, value: str, *args: Any, **kwargs: Any) -> Any:
        return value


class IntegerMap(MappedField, Integer):
    def _deserialize(self, *args: Any, **kwargs: Any) -> Any:
        result = super()._deserialize(*args, **kwargs)
        return IntegerMapping(*result)

    def _serialize(self, *args: Any, **kwargs: Any) -> Any:
        return super()._serialize(*args, **kwargs)

    _tuple_fields = Integer(), String()


class StringMap(MappedField, String):
    def _deserialize(self, *args: Any, **kwargs: Any) -> Any:
        result = super()._deserialize(*args, **kwargs)
        return StringMapping(*result)

    def _serialize(self, *args: Any, **kwargs: Any) -> Any:
        return super()._serialize(*args, **kwargs)

    _tuple_fields = String(), String()
