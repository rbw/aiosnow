from abc import abstractmethod

import marshmallow
import ujson

from .operators import StringOperator
from .query import Condition

_fields = marshmallow.fields


class BaseField(marshmallow.fields.String):
    pass


class Text(BaseField):
    def eq(self, value):
        return Condition(self.name, StringOperator.EQUALS, value)


class SchemaOpts(marshmallow.schema.SchemaOpts):
    def __init__(self, meta, **kwargs):
        self.load_only = []
        self.dump_only = []

        super(SchemaOpts, self).__init__(meta, **kwargs)
        self.render_module = ujson
        self.unknown = marshmallow.EXCLUDE


class SchemaMeta(marshmallow.schema.SchemaMeta):
    def __new__(mcs, name, bases, attrs):
        fields = [item for item in attrs.items() if isinstance(item[1], BaseField)]
        klass = super().__new__(mcs, name, bases, attrs)

        for name, field in fields:
            field.name = name
            setattr(klass, name, field)

        return klass


class Schema(marshmallow.Schema, metaclass=SchemaMeta):
    OPTIONS_CLASS = SchemaOpts

    @property
    def __location__(self):
        raise NotImplementedError

    __resolve__ = True
