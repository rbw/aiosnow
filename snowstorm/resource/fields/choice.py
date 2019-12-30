from snowstorm.query import BaseOperator

from .text import Text
from .numeric import Numeric


class NumericChoice(Numeric):
    pass


class TextChoice(Text):
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
