from functools import partial

import marshmallow

from snowstorm.query import Segment, String
from snowstorm.exceptions import UnexpectedValue


class BaseField(marshmallow.fields.String):
    def _segment(self, operator, value=None, field_operator=None):
        if isinstance(value, BaseField):
            if not field_operator:
                raise UnexpectedValue(f"{operator} does not support field comparison")

            operator = field_operator
            value = value.name

        return Segment(self.name, operator, value)

    def equals(self, value):
        """
        All records in which the Short description says nothing else but "Network storage is unavailable."
        """

        return self._segment(String.EQUALS, value, field_operator=String.SAME)

    def not_equals(self, value):
        """
        All records in which the value for the Short description field says anything but "Network storage
        is unavailable."
        """

        return self._segment(String.NOT_EQUALS, value, field_operator=String.DIFFERENT)

    def is_empty(self):
        return self._segment(String.EMPTY)

    def is_populated(self):
        return self._segment(String.POPULATED)
