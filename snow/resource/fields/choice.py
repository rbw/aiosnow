from .text import Text
from .numeric import Numeric
from .base import BaseField


class ChoiceBase(BaseField):
    pass


class NumericChoice(ChoiceBase, Numeric):
    pass


class TextChoice(ChoiceBase, Text):
    pass
