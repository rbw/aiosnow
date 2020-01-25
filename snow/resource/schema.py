import warnings

from typing import Tuple, Iterable

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

            # Register queryable BaseField with the class.
            setattr(cls, name, field)

        return cls


class Schema(marshmallow.Schema, metaclass=SchemaMeta):
    """Resource schema

    Attributes:
        __location__: API path
    """

    OPTIONS_CLASS = SchemaOpts

    def __init__(self, *args, **kwargs):
        super(Schema, self).__init__(*args, **kwargs)

    def __transform(self, data: dict) -> Iterable[Tuple[str, str]]:
        for key, value in data.items():
            name = key.name if isinstance(key, BaseField) else key

            if isinstance(value, dict):
                field = getattr(self, name, None)
                if not field:
                    warnings.warn(f"Unexpected field in response content: {name}, skipping...")
                    continue

                yield name, value[field.joined.value]
            else:
                yield name, value

    @marshmallow.pre_load
    def _transform(self, data, **_):
        """Normalize the given data

        Args:
            data: Dictionary of fields to load

        Returns:
            dict(field_name=field_value, ...)
        """

        return dict(self.__transform(data))

    @property
    def __location__(self):
        raise NotImplementedError
