from datetime import datetime

from snowstorm.query import DateTimeOperator

from .base import BaseField


class Datetime(BaseField):
    def before(self, value):
        """
        Example: sla_due.on("2019-12-24 02:03:04")

        All records in which the value for the SLA due field is any datetime previous to "2019-12-24 02:03:04".
        """

        if isinstance(value, datetime):
            dt_str = value.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(value, str):
            dt_str = value
        else:
            raise TypeError(f"Expected a string or datetime.datetime in {self}, got: {value}")

        return self._segment(DateTimeOperator.ON, f'javascript:gs.dateGenerate("{dt_str}")')
