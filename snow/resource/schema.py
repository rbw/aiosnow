import marshmallow
import ujson
import warnings

from typing import Iterable, Tuple

from snow.exceptions import NoSchemaFields

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
            elif isinstance(value, SchemaMeta):
                fields[key] = Nested(key, value, allow_none=True, required=False)

        attrs.update(fields)
        cls = super().__new__(mcs, name, bases, attrs)

        for name, field in fields.items():
            value = field

            if not isinstance(value, Nested):
                value.name = name

            setattr(cls, name, value)

        return cls


class Nested(marshmallow.fields.Nested):
    def __init__(self, parent_name, nested_cls, *args, **kwargs):
        # Set namespace to support nested queries
        for name, field in getattr(nested_cls, "_declared_fields").items():
            field.name = f"{parent_name}.{name}"
            setattr(self, name, field)

        super(Nested, self).__init__(nested_cls, *args, **kwargs)


class Schema(marshmallow.Schema, metaclass=SchemaMeta):
    """Resource schema

    Attributes:
        __location__: API path
    """

    OPTIONS_CLASS = SchemaOpts
    joined_with: str = None

    def __init__(self, *args, joined_with: str = None, **kwargs):
        self.registered_fields = self.get_fields()
        self.nested_fields = [k for k, v in self.registered_fields.items() if isinstance(v, Nested)]

        if joined_with:
            self.joined_with = joined_with

            # Enable automatic dot-walking of joined fields
            for field in self.get_fields().values():
                field.name = f"{joined_with}.{field.name}"

        super(Schema, self).__init__(*args, **kwargs)

    @classmethod
    def get_fields(cls):
        fields = {}
        for name, field in cls.__dict__.items():
            if name.startswith("_") or name == "opts":
                continue

            fields[name] = field

        if not fields:
            raise NoSchemaFields(f"Schema {cls} lacks fields definitions")

        return fields

    def __transform_response(self, data) -> Iterable[Tuple[str, str]]:
        """Transform the response after ensuring its sanity

        Args:
            data: Response content

        Yields: <name>, <value>
        """

        for key, value in data.items():
            field = self.registered_fields.get(key, None)

            if isinstance(field, BaseField):
                name = field.name

                if isinstance(value, str):
                    pass
                elif isinstance(value, dict) and {"value", "display_value"} <= set(value.keys()):
                    if not getattr(self, name, None):
                        warnings.warn(f"Unexpected field in response content: {name}, skipping...")
                        continue

                    yield name, value[field.joined.value]
                    continue
            elif isinstance(field, Nested):
                pass
            else:  # Unknown field
                continue

            yield key, value

    @marshmallow.pre_load
    def _transform(self, data, **_):
        """Normalize the given data

        Args:
            data: Dictionary of fields to load

        Returns:
            dict(field_name=field_value, ...)
        """

        return dict(self.__transform_response(data or {}))

    @property
    def __location__(self):
        raise NotImplementedError


class PartialSchema(Schema):
    @property
    def __location__(self):
        return None
