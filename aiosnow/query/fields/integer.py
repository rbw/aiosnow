from aiosnow.query.condition import Condition
from aiosnow.query.operators import IntegerOperator

from .base import BaseQueryable


class IntegerQueryable(BaseQueryable):
    def equals(self, value: int) -> Condition:
        """
        Example: reassignment_count.equals(0)

        All records in which the Reassignment count is nothing else but 0.
        """

        return self._condition(
            IntegerOperator.EQUALS, value, field_operator=IntegerOperator.SAME
        )

    def not_equals(self, value: int) -> Condition:
        """
        Example: reassignment_count.not_equals(0)

        All records in which the value for the Reassignment count is any number but 0.
        """

        return self._condition(
            IntegerOperator.NOT_EQUALS, value, field_operator=IntegerOperator.DIFFERENT
        )

    def less_than(self, value: int) -> Condition:
        """
        Example: impact.less_than(2)

        All records in which the Impact field has a value of 1 - High.
        """

        return self._condition(
            IntegerOperator.LESS, value, field_operator=IntegerOperator.Related.LESS
        )

    def greater_than(self, value: int) -> Condition:
        """
        Example: impact.greater_than(2)

        All records in which the Impact field has a value of 3 - Low
        """

        return self._condition(
            IntegerOperator.GREATER,
            value,
            field_operator=IntegerOperator.Related.GREATER,
        )

    def less_or_equals(self, value: int) -> Condition:
        """
        Example: impact.less_or_equals(2)

        All records in which the Impact field has a value of 1 - High or 2 - Medium.
        """

        return self._condition(
            IntegerOperator.LESS_EQUALS,
            value,
            field_operator=IntegerOperator.Related.LESS_EQUALS,
        )

    def greater_or_equals(self, value: int) -> Condition:
        """
        Example: impact.greater_or_equals(2)

        All records in which the Impact field has a value of 2 - Medium or 3 - Low.
        """

        return self._condition(
            IntegerOperator.GREATER_EQUALS,
            value,
            field_operator=IntegerOperator.Related.GREATER_EQUALS,
        )

    def between(self, value1: int, value2: int) -> Condition:
        """
        Example: impact.between([1, 3])

        All records in which the Impact field has one of the following values:
        1 - High
        2 - Medium
        3 - Low
        """

        value = f"{value1}@{value2}"
        return self._condition(IntegerOperator.BETWEEN, value)
