import warnings

import marshmallow
import ujson

from .fields import BaseField


class SchemaOpts(marshmallow.schema.SchemaOpts):
    def __init__(self, meta, **kwargs):
        self.load_only = []
        self.dump_only = []

        super(SchemaOpts, self).__init__(meta, **kwargs)
        self.render_module = ujson
        self.unknown = marshmallow.EXCLUDE


class SchemaMeta(marshmallow.schema.SchemaMeta):
    def __new__(mcs, name, bases, attrs):
        fields = {}
        for key, value in attrs.items():
            if isinstance(value, BaseField):
                fields[key] = value

        cls = super().__new__(mcs, name, bases, attrs)

        for name, field in fields.items():
            field.name = name
            setattr(cls, name, field)

        return cls


class Schema(marshmallow.Schema, metaclass=SchemaMeta):
    OPTIONS_CLASS = SchemaOpts

    def _link_fields(self, fields):
        for key, value in fields.items():
            name = key.name if isinstance(key, BaseField) else key
            field = getattr(self, name, None)
            if not field:
                warnings.warn(f"Unexpected field in response content: {name}, skipping...")
                continue

            if isinstance(value, dict):
                yield name, value[field.joined.value]
            else:
                yield name, value

    @marshmallow.pre_load
    def pre_load(self, data, **kwargs):
        return dict(self._link_fields(data))

    @property
    def __location__(self):
        raise NotImplementedError
