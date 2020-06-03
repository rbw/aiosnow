from .base import BaseField
from .integer import Integer
from .string import String


class NumericChoice(Integer, BaseField):
    pass


class TextChoice(String, BaseField):
    pass
