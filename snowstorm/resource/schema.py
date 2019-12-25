import marshmallow
import ujson

from .operators import StringOperator
from .query import Condition

_fields = marshmallow.fields


class TextField(marshmallow.fields.String):
    operator = StringOperator

    def __init__(self, *args, **kwargs):
        super(TextField, self).__init__(*args, **kwargs)

    def eq(self, value):
        return Condition(self.name, StringOperator.EQUALS, value)


class Text(TextField):
    pass


class SchemaOpts(marshmallow.schema.SchemaOpts):
    def __init__(self, meta, **kwargs):
        self.load_only = []
        self.dump_only = []

        super(SchemaOpts, self).__init__(meta, **kwargs)
        self.render_module = ujson
        self.unknown = marshmallow.EXCLUDE


class Schema(marshmallow.Schema):
    OPTIONS_CLASS = SchemaOpts

    @property
    def __location__(self):
        raise NotImplementedError

    __resolve__ = True
