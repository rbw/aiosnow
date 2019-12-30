from datetime import datetime

from snowstorm.query import DateTimeOperator

from .base import BaseField


class Datetime(BaseField):
    def _segment(self, *args, value=None, **kwargs):
        if isinstance(value, datetime):
            dt_str = value.strftime("%Y-%m-%d")
        elif isinstance(value, str):
            dt_str = value
        elif value is None:
            dt_str = None
        else:
            raise TypeError(f"Expected a string or datetime.datetime in {self}, got: {value}")

        super(Datetime, self)._segment(*args, value=dt_str, **kwargs)

    def on(self, value):
        """
        Example: sla_due.on("2019-12-24 02:03:04")

        All records in which the value for the SLA due field matches the given date
        """

        return self._segment(DateTimeOperator.ON, value)

    def not_on(self, value):
        """
        Example: sla_due.not_on("2019-12-24 02:03:04")

        All records in which the value for the SLA due field is any other but the given date
        """

        return self._segment(DateTimeOperator.NOT_ON, value)

    def before(self, value):
        """
        Example: sla_due.before("2019-12-24 02:03:04")

        All records in which the value for the SLA due field is any date previous to the given date.
        """

        return self._segment(DateTimeOperator.LESS, value)

    def after(self, value):
        """
        Example: sla_due.after("2019-12-24 02:03:04")

        All records in which the value for the SLA due field is any date after the given date.
        """

        return self._segment(DateTimeOperator.GREATER, value)

    def until(self, value):
        """
        Example: sla_due.until("2019-12-24 02:03:04")

        All records in which the value for the SLA due field is one of the following:
            - any date previous to today
            - today
        """

        return self._segment(DateTimeOperator.LESS_EQUALS, value)

    def as_of(self, value):
        """
        Example: sla_due.as_of("2019-12-24 02:03:04")

        All records in which the date value for the SLA due field is one of the following:
            - today
            - any date after today
        """

        return self._segment(DateTimeOperator.GREATER_EQUALS, value)

    def between(self, value1, value2):
        """
        Example:

        All records in which the value for the SLA due field is between the given dates
        """

        return self._segment(DateTimeOperator.BETWEEN, f"{value1}@{value2}")
