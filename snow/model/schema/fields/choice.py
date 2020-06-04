from .base import BaseField
from .integer import Integer
from .string import String


class IntegerChoice(Integer, BaseField):
    pass


class StringChoice(String, BaseField):
    pass
