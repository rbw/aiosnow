import marshmallow
import ujson

from .query import QueryBuilder

_fields = marshmallow.fields


class QueryMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(QueryMeta, cls).__call__(*args, **kwargs)

        return cls._instances[cls]


class String(_fields.String, QueryBuilder):
    pass


class SchemaOpts(marshmallow.schema.SchemaOpts):
    def __init__(self, meta, **kwargs):
        self.load_only = []
        self.dump_only = []

        super(SchemaOpts, self).__init__(meta, **kwargs)
        self.render_module = ujson
        self.unknown = marshmallow.EXCLUDE


class SchemaMeta(marshmallow.schema.SchemaMeta):
    def __new__(mcs, name, bases, attrs):
        cls = super().__new__(mcs, name, bases, attrs)
        for name, field in cls._declared_fields.items():
            setattr(cls, name, QueryBuilder(name))

        return cls


class Schema(marshmallow.Schema, metaclass=SchemaMeta):
    OPTIONS_CLASS = SchemaOpts

    @property
    def __location__(self):
        raise NotImplementedError

    __resolve__ = True
