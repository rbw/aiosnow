from snowstorm.query import String

from .base import BaseField


class Numeric(BaseField):
    def between(self, value):
        """
        All records in which the Impact field has one of the following values:
            1 - High
            2 - Medium
            3 - Low
        """

        return self._segment(String.BETWEEN, value)

    def lt_than(self, value):
        """
        All records in which the Impact field has a value of 1 - High.
        """

        return self._segment(String.LESS, value)

    def gt_than(self, value):
        """
        All records in which the Impact field has a value of 3 - Low
        """

        return self._segment(String.GREATER, value)

    def le_than(self, value):
        """
        All records in which the Impact field has a value of 1 - High or 2 - Medium.
        """

        return self._segment(String.LESS_EQUAL, value)

    def ge_than(self, value):
        """
        All records in which the Impact field has a value of 2 - Medium or 3 - Low.
        """

        return self._segment(String.GREATER_EQUAL, value)
