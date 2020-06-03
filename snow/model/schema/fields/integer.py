import warnings
from typing import Any

import marshmallow

from snow.query import Condition, NumericOperator

from .base import BaseField


class Integer(marshmallow.fields.Integer, BaseField):
    def equals(self, value: int) -> Condition:
        """
        Example: reassignment_count.equals(0)

        All records in which the Reassignment count is nothing else but 0.
        """

        return self._condition(
            NumericOperator.EQUALS, value, field_operator=NumericOperator.SAME
        )

    def not_equals(self, value: int) -> Condition:
        """
        Example: reassignment_count.not_equals(0)

        All records in which the value for the Reassignment count is any number but 0.
        """

        return self._condition(
            NumericOperator.NOT_EQUALS, value, field_operator=NumericOperator.DIFFERENT
        )

    def less_than(self, value: int) -> Condition:
        """
        Example: impact.less_than(2)

        All records in which the Impact field has a value of 1 - High.
        """

        return self._condition(
            NumericOperator.LESS, value, field_operator=NumericOperator.Related.LESS
        )

    def greater_than(self, value: int) -> Condition:
        """
        Example: impact.greater_than(2)

        All records in which the Impact field has a value of 3 - Low
        """

        return self._condition(
            NumericOperator.LESS, value, field_operator=NumericOperator.Related.GREATER
        )

    def less_or_equals(self, value: int) -> Condition:
        """
        Example: impact.less_or_equals(2)

        All records in which the Impact field has a value of 1 - High or 2 - Medium.
        """

        return self._condition(
            NumericOperator.LESS,
            value,
            field_operator=NumericOperator.Related.LESS_EQUALS,
        )

    def greater_or_equals(self, value: int) -> Condition:
        """
        Example: impact.greater_or_equals(2)

        All records in which the Impact field has a value of 2 - Medium or 3 - Low.
        """

        return self._condition(
            NumericOperator.GREATER_EQUALS,
            value,
            field_operator=NumericOperator.Related.GREATER_EQUALS,
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
        return self._condition(NumericOperator.BETWEEN, value)


class Numeric(Integer):
    def __init__(self, *args: Any, **kwargs: Any):
        warnings.warn(
            "Numeric is deprecated, please use Integer instead", DeprecationWarning,
        )
        super(Numeric, self).__init__(*args, **kwargs)
