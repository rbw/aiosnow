from functools import partial

import marshmallow

from snowstorm.query import Segment, BaseOperator
from snowstorm.exceptions import UnexpectedValue


class BaseField(marshmallow.fields.Field):
    def _segment(self, operator, value=None, field_operator=None):
        if isinstance(value, BaseField):
            if not field_operator:
                raise UnexpectedValue(f"{operator} does not support field comparison")

            operator = field_operator
            value = value.name

        return Segment(self.name, operator, value)

    def is_empty(self):
        """
        All records in which there is no value in the given field
        """

        return self._segment(BaseOperator.EMPTY)

    def is_populated(self):
        """
        All records in which there is any value in the given field
        """

        return self._segment(BaseOperator.POPULATED)

    def is_anything(self):
        """
        All records in which the given field is one of the following:
            - any value
            - empty
            - NULL
        """

        return self._segment(BaseOperator.ANYTHING)
