import marshmallow

from snow.exceptions import UnexpectedValue
from snow.consts import Joined

from ..query import Condition, BaseOperator


class BaseField(marshmallow.fields.Field):
    def __init__(self, *args, pluck=Joined.VALUE, is_primary=False, **kwargs):
        self.joined = Joined(pluck)
        self.is_primary = is_primary
        super(BaseField, self).__init__(*args, **kwargs)

    def _condition(self, operator, value=None, field_operator=None):
        if isinstance(value, BaseField):
            if not field_operator:
                raise UnexpectedValue(f"{operator} does not support Field comparison")

            operator = field_operator
            value = value.name

        return Condition(self.name, operator, value)

    def in_list(self, value):
        """
        Example: impact.in_list([3, 4])

        All records in which the Impact field has one of the values 3 or 4.
        """

        value = ",".join(str(v) for v in value)
        return self._condition(BaseOperator.ONEOF, value)

    def not_in_list(self, value):
        """
        Example: impact.not_in_list([3, 4])

        All records in which the Impact field does not have one of the values 3 or 4.
        """

        value = ",".join(str(v) for v in value)
        return self._condition(BaseOperator.NOT_ONEOF, value)

    def is_empty(self):
        """
        All records in which there is no value in the given field
        """

        return self._condition(BaseOperator.EMPTY)

    def is_populated(self):
        """
        All records in which there is any value in the given field
        """

        return self._condition(BaseOperator.POPULATED)

    def is_anything(self):
        """
        All records in which the given field is one of the following:
            - any value
            - empty
            - NULL
        """

        return self._condition(BaseOperator.ANYTHING)
