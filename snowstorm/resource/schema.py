import marshmallow
import ujson

from .fields.base import BaseField


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
        cls = super().__new__(mcs, name, bases, attrs)

        for name, field in fields:
            field.name = name
            setattr(cls, name, field)

        return cls


class Schema(marshmallow.Schema, metaclass=SchemaMeta):
    OPTIONS_CLASS = SchemaOpts

    @property
    def __location__(self):
        raise NotImplementedError

    __resolve__ = True
