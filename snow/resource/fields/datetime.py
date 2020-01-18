import marshmallow

from .base import BaseField

from ..query import DateTimeOperator


class Datetime(BaseField, marshmallow.fields.DateTime):
    def _segment(self, operator, value=None, **kwargs):
        # @TODO - add support for "DatetimeHelper" and serialize here.
        return super(Datetime, self)._segment(operator, value, **kwargs)

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
