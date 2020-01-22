from .base import BaseField

from ..query import EmailOperator


class Email(BaseField):
    def changes(self):
        """
        Example: state.changes()

        All records in which the State field is updated.
        """

        return self._segment(EmailOperator.CHANGES)

    def changes_from(self, value):
        """
        Example: state.changes_from("4^EQ")

        All records in which the State field is updated to another value after previously being Awaiting User Info.
        """

        return self._segment(EmailOperator.CHANGES_FROM, value)

    def changes_to(self, value):
        """
        Example: state.changes_to("4^EQ")

        All records in which the State field is updated to Awaiting User Info after previously being any other value.
        """

        return self._segment(EmailOperator.CHANGES_TO, value)
