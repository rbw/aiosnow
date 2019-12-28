from snowstorm.query import String

from .base import BaseField


class Text(BaseField):
    def contains(self, value):
        """
        All records in which the characters "SAP" appear anywhere in the value for the Short description field.
        """

        return self._segment(String.CONTAINS, value)

    def not_contains(self, value):
        """
        All records in which the characters "SAP" do not appear anywhere in the value for the Short description field.
        """

        return self._segment(String.NOT_CONTAINS, value)

    def between(self, value1, value2):
        """
        All records in which the first letter in the Short description field is "q," "r," "s," or "t."
        """

        value = f"{value1}@{value2}"
        return self._segment(String.BETWEEN, value)
