from .text import Text
from .numeric import Numeric
from .base import BaseField


class NumericChoice(BaseField, Numeric):
    pass


class TextChoice(BaseField, Text):
    pass
