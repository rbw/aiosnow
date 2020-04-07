import marshmallow

from snow.exceptions import UnexpectedValue
from snow.consts import Joined

from ..query import Condition, BaseOperator

from ._utils import serialize_list


class BaseField(marshmallow.fields.Field):
    def __init__(self, *args, pluck=Joined.VALUE, is_primary=False, empty_as_none=True, **kwargs):
        self.joined = Joined(pluck)
        self.is_primary = is_primary
        self.empty_as_none = empty_as_none
        super(BaseField, self).__init__(*args, **kwargs)
        self.allow_none = kwargs.pop("allow_none", True)

    def _deserialize(self, value, *args, **kwargs):
        if self.empty_as_none and value == "":
            return None

        return value

    def _condition(self, operator, value=None, field_operator=None):
        if isinstance(value, BaseField):
            if not field_operator:
                raise UnexpectedValue(f"{operator} does not support Field comparison")

            operator = field_operator
            value = value.name

        return Condition(self.name, operator, value)

    def in_list(self, values):
        """
        Example: impact.in_list([3, 4])

        All records in which the Impact field has one of the values 3 or 4.
        """

        return self._condition(BaseOperator.ONEOF, serialize_list(values))

    def not_in_list(self, values):
        """
        Example: impact.not_in_list([3, 4])

        All records in which the Impact field does not have one of the values 3 or 4.
        """

        return self._condition(BaseOperator.NOT_ONEOF, serialize_list(values))

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
