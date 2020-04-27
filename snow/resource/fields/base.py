from typing import Any, Union

import marshmallow

from snow.consts import Joined
from snow.exceptions import SnowException, UnexpectedValue

from ..query import BaseOperator, Condition
from ._utils import serialize_list


class BaseField(marshmallow.fields.Field):
    def __init__(
        self,
        *args: Any,
        pluck: Joined = Joined.VALUE,
        is_primary: bool = False,
        **kwargs: Any,
    ):
        self.joined = Joined(pluck)
        self.is_primary = is_primary
        super(BaseField, self).__init__(*args, **kwargs)
        self.allow_none = kwargs.pop("allow_none", True)

    def _condition(
        self, operator: str, value: Union[str, int] = None, field_operator: str = ""
    ) -> Condition:
        if isinstance(value, BaseField):
            if not field_operator:
                raise UnexpectedValue(f"{operator} does not support Field comparison")

            operator = field_operator
            value = value.name

        if not isinstance(self.name, str):
            raise SnowException(f"Missing left operand of {self.__class__}")

        return Condition(self.name, operator, value)

    def in_list(self, values: list) -> Condition:
        """
        Example: impact.in_list([3, 4])

        All records in which the Impact field has one of the values 3 or 4.
        """

        return self._condition(BaseOperator.ONEOF, serialize_list(values))

    def not_in_list(self, values: list) -> Condition:
        """
        Example: impact.not_in_list([3, 4])

        All records in which the Impact field does not have one of the values 3 or 4.
        """

        return self._condition(BaseOperator.NOT_ONEOF, serialize_list(values))

    def is_empty(self) -> Condition:
        """
        All records in which there is no value in the given field
        """

        return self._condition(BaseOperator.EMPTY)

    def is_populated(self) -> Condition:
        """
        All records in which there is any value in the given field
        """

        return self._condition(BaseOperator.POPULATED)

    def is_anything(self) -> Condition:
        """
        All records in which the given field is one of the following:
            - any value
            - empty
            - NULL
        """

        return self._condition(BaseOperator.ANYTHING)
