import marshmallow

from .base import BaseField

from ..query import StringOperator


class Text(BaseField, marshmallow.fields.String):
    def equals(self, value):
        """
        Example: short_description.equals("Network storage is unavailable")

        All records in which the Short description says nothing else but "Network storage is unavailable."
        """

        return self._segment(StringOperator.EQUALS, value, field_operator=StringOperator.SAME)

    def not_equals(self, value):
        """
        Example: short_description.not_equals("Network storage is unavailable")

        All records in which the value for the Short description field says anything but "Network storage
        is unavailable."
        """

        return self._segment(StringOperator.NOT_EQUALS, value, field_operator=StringOperator.DIFFERENT)

    def starts_with(self, value):
        """
        Example: short_description.starts_with("SAP")

        All records in which the characters "SAP" appear at the beginning of the value for the Short description field.
        """

        return self._segment(StringOperator.STARTSWITH, value)

    def ends_with(self, value):
        """
        Example: short_description.ends_with("outage")

        All records in which the string "outage" appears at the end of the value for the Short description field.
        """

        return self._segment(StringOperator.ENDSWITH, value)

    def contains(self, value):
        """
        Example: short_description.contains("SAP")

        All records in which the characters "SAP" appear anywhere in the value for the Short description field.
        """

        return self._segment(StringOperator.CONTAINS, value)

    def not_contains(self, value):
        """
        Example: short_description.not_contains("SAP")

        All records in which the characters "SAP" do not appear anywhere in the value for the Short description field.
        """

        return self._segment(StringOperator.NOT_CONTAINS, value)

    def less_or_equals(self, value):
        """
        Example: short_description.less_or_equals("s")

        All records in which the string in the Short description field is one of the following:
            - the first letter is any letter between "a" and "s"
            - the exact value is "s"
        """

        return self._segment(StringOperator.LESS_EQUALS, value)

    def greater_or_equals(self, value):
        """
        Example: short_description.greater_or_equals("s")

        All records in which the string in the Short description field is one of the following:
            - the first letter is any letter between "s" and "z"
            - the exact value is "s"
        """

        return self._segment(StringOperator.GREATER_EQUALS, value)

    def between(self, value1, value2):
        """
        Example: short_description.between("q", "t")

        All records in which the first letter in the Short description field is "q," "r," "s," or "t."
        """

        value = f"{value1}@{value2}"
        return self._segment(StringOperator.BETWEEN, value)
