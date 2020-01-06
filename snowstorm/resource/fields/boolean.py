from .base import BaseField

from ..query import BooleanOperator


class Boolean(BaseField):
    def is_true(self):
        """
        Example: active.is_true()

        All records in which the Active field is True.
        """

        return self._segment(BooleanOperator.EQUALS, "true")

    def is_falsy(self):
        """
        Example: active.is_falsy()

        All records in which the Active field is False, empty, or NULL.
        """

        return self._segment(BooleanOperator.NOT_EQUALS, "true")
