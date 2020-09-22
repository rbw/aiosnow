from aiosnow.query.condition import Condition
from aiosnow.query.operators import BooleanOperator

from .base import BaseQueryable


class BooleanQueryable(BaseQueryable):
    def is_true(self) -> Condition:
        """
        Example: active.is_true()

        All records in which the Active field is True.
        """

        return self._condition(BooleanOperator.EQUALS, "true")

    def is_falsy(self) -> Condition:
        """
        Example: active.is_falsy()

        All records in which the Active field is False, empty, or NULL.
        """

        return self._condition(BooleanOperator.NOT_EQUALS, "true")
