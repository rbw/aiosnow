from .base import BaseField
from .numeric import Numeric
from .text import Text


class NumericChoice(Numeric, BaseField):
    pass


class TextChoice(Text, BaseField):
    pass
