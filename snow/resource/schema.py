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

    Defines a Resource's entities and the relationship among them.

    Attributes:
        __location__ (str): API path
    """

    OPTIONS_CLASS = SchemaOpts

    def _consume(self, data: dict) -> Iterable[Tuple[str, str]]:
        """Consumes the to-be-loaded items

        - Plucks joined targets
        - Warns if an unexpected field was encountered

        Args:
            data: Dictionary of fields to load

        Yields:
            (field_name, field_value)

        """

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
    def transform(self, data, **_):
        return dict(self._consume(data))

    @property
    def __location__(self):
        raise NotImplementedError
