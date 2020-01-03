import warnings

import marshmallow
import ujson

from snowstorm.consts import Target

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
        for name, record in fields.items():
            field = getattr(self, name, None)
            if not field:
                warnings.warn(f"Unexpected field in response content: {name}, skipping...")
                continue

            if isinstance(record, dict):
                yield name, record[field.target.value]
            else:
                yield name, record

    @marshmallow.pre_load
    def pre_load(self, data, **kwargs):
        return dict(self._link_fields(data))

    @property
    def __location__(self):
        raise NotImplementedError
