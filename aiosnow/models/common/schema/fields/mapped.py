from abc import ABC
from typing import Any, Tuple, Union

import marshmallow

from .integer import Integer
from .string import String


class Mapping(ABC):
    key: Union[str, int, None] = None
    value: Union[str, None] = None

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} [key={self.key}, value={self.value}]>"


class StringMapping(Mapping):
    def __init__(self, key: str, value: str):
        self.key = key
        self.value = value


class IntegerMapping(Mapping):
    def __init__(self, key: int, value: str):
        self.key = key
        self.value = value


class MappedField(marshmallow.fields.Tuple):
    def __init__(self, *args: Any, dump_text: bool = False, **kwargs: Any):
        self.should_dump_text = dump_text
        super(MappedField, self).__init__(self._tuple_fields, *args, **kwargs)

    @property
    def _tuple_fields(self) -> Tuple[Union[Integer, String], String]:
        raise NotImplementedError

    def _serialize(self, *args: Any, **kwargs: Any) -> Any:
        obj = args[0]

        if self.should_dump_text:
            return obj.value

        return obj.key


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
