from snowstorm.query import DateTimeOperator

from .base import BaseField


class Datetime(BaseField):
    def on(self, value):
        """
        Example: sla_due.on()

        All records in which the value for the SLA due field matches the date for today.
        """

        return self._segment(DateTimeOperator.ON, value)
