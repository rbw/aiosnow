from aiosnow.query.condition import Condition
from aiosnow.query.operators import DateTimeOperator

from .base import BaseQueryable


class DateTimeQueryable(BaseQueryable):
    def on(self, value: str) -> Condition:
        """
        Example: sla_due.on("2019-12-24 02:03:04")

        All records in which the value for the SLA due field matches the given date
        """

        return self._condition(DateTimeOperator.ON, value)

    def not_on(self, value: str) -> Condition:
        """
        Example: sla_due.not_on("2019-12-24 02:03:04")

        All records in which the value for the SLA due field is any other but the given date
        """

        return self._condition(DateTimeOperator.NOT_ON, value)

    def before(self, value: str) -> Condition:
        """
        Example: sla_due.before("2019-12-24 02:03:04")

        All records in which the value for the SLA due field is any date previous to the given date.
        """

        return self._condition(DateTimeOperator.LESS, value)

    def after(self, value: str) -> Condition:
        """
        Example: sla_due.after("2019-12-24 02:03:04")

        All records in which the value for the SLA due field is any date after the given date.
        """

        return self._condition(DateTimeOperator.GREATER, value)

    def until(self, value: str) -> Condition:
        """
        Example: sla_due.until("2019-12-24 02:03:04")

        All records in which the value for the SLA due field is one of the following:
            - any date previous to today
            - today
        """

        return self._condition(DateTimeOperator.LESS_EQUALS, value)

    def as_of(self, value: str) -> Condition:
        """
        Example: sla_due.as_of("2019-12-24 02:03:04")

        All records in which the date value for the SLA due field is one of the following:
            - today
            - any date after today
        """

        return self._condition(DateTimeOperator.GREATER_EQUALS, value)

    def between(self, value1: str, value2: str) -> Condition:
        """
        Example:

        All records in which the value for the SLA due field is between the given dates
        """

        return self._condition(DateTimeOperator.BETWEEN, f"{value1}@{value2}")
