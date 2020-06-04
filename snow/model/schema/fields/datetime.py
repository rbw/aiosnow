import warnings
from typing import Any

import marshmallow

from snow.query import Condition, DateTimeOperator

from .base import BaseField


class DateTime(marshmallow.fields.DateTime, BaseField):
    def _bind_to_schema(self, field_name: str, schema: marshmallow.Schema) -> None:
        """Removing this override causes marshmallow schema-field registration to fail
        because self.root resolves to None when inheriting schemas? This
        seems exclusive to the DateTime type, and could be a marshmallow bug.

        "AttributeError: 'NoneType' object has no attribute 'opts'"

        @TODO - find out why DateTime schema parent fails to resolve for DateTime and remove this override"""

        self.format = (
            self.format
            or getattr(schema.opts, self.SCHEMA_OPTS_VAR_NAME)
            or self.DEFAULT_FORMAT
        )

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


class Datetime(DateTime):
    def __init__(self, *args: Any, **kwargs: Any):
        warnings.warn(
            "Datetime is deprecated, please use DateTime instead", DeprecationWarning,
        )
        super(Datetime, self).__init__(*args, **kwargs)
