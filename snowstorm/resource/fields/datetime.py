from datetime import datetime

import marshmallow
import pytz

from snowstorm.query import DateTimeOperator

from .base import BaseField


class Datetime(BaseField, marshmallow.fields.DateTime):
    def _get_datetime(self, value):
        if isinstance(value, datetime):
            dt_obj = value.astimezone(pytz.UTC)
        elif isinstance(value, str):
            dt_obj = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
            date = dt_obj.strftime("%Y-%m-%d")
            time = dt_obj.strftime("%H:%M:%S")
            dt_obj = f'javascript:gs.dateGenerate("{date}", "{time}")'
        elif value is None:
            dt_obj = None
        else:
            raise TypeError(f"Expected a string or datetime.datetime in {self}, got: {value}")

        return dt_obj

    def _segment(self, operator, value=None, **kwargs):
        # dt_str = f'javascript:gs.dateGenerate("{dt_str}")'
        dt_str = self._get_datetime(value)
        print(dt_str)
        return super(Datetime, self)._segment(operator, value=dt_str, **kwargs)

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
