from .text import Text
from .numeric import Numeric
from .base import BaseField


class NumericChoice(Numeric, BaseField):
    pass


class TextChoice(Text, BaseField):
    pass
