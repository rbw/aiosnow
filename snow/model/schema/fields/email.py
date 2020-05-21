import marshmallow

from snow.query import Condition, EmailOperator

from .base import BaseField


class Email(marshmallow.fields.Email, BaseField):
    def changes(self) -> Condition:
        """
        Example: state.changes()

        All records in which the State field is updated.
        """

        return self._condition(EmailOperator.CHANGES)

    def changes_from(self, value: str) -> Condition:
        """
        Example: state.changes_from("4^EQ")

        All records in which the State field is updated to another value after previously being Awaiting User Info.
        """

        return self._condition(EmailOperator.CHANGES_FROM, value)

    def changes_to(self, value: str) -> Condition:
        """
        Example: state.changes_to("4^EQ")

        All records in which the State field is updated to Awaiting User Info after previously being any other value.
        """

        return self._condition(EmailOperator.CHANGES_TO, value)
