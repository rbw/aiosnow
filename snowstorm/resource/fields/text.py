from snowstorm.query import Segment, StringOperator

from .base import BaseField


class Text(BaseField):
    def eq(self, value):
        return Segment(self.name, StringOperator.EQUALS, value)
