from snowstorm.query import BaseOperator

from .base import BaseField
from .text import Text
from .numeric import Numeric


class ChoiceBase(BaseField):
    def oneof(self, *values):
        """
        All records in which the field is populated by the given values
        """

        return self._segment(BaseOperator.ONEOF, ",".join(values))

    def not_oneof(self, *values):
        """
        All records in which the field is not populated by the given values
        """

        return self._segment(BaseOperator.NOT_ONEOF, ",".join(values))


class NumericChoice(ChoiceBase, Numeric):
    pass


class TextChoice(ChoiceBase, Text):
    pass
