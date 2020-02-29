import marshmallow
import ujson

from snow.exceptions import NoSchemaFields

from .fields import BaseField, Nested


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
                fields[key] = Nested(value)

        cls = super().__new__(mcs, name, bases, attrs)

        for name, field in fields.items():
            value = field
            value.name = name

            setattr(cls, name, value)

        return cls


class Schema(marshmallow.Schema, metaclass=SchemaMeta):
    """Resource schema

    Attributes:
        __location__: API path
    """

    OPTIONS_CLASS = SchemaOpts
    joined_with: str = None
    resource = None

    def __init__(self, *args, joined_with: str = None, **kwargs):
        if joined_with:
            self.joined_with = joined_with

            for field in self.get_fields().values():
                # Refer to field as a child of `joined_with` when querying
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

    @marshmallow.pre_load
    def _transform(self, data, **_):
        """Normalize the given data

        Args:
            data: Dictionary of fields to load

        Returns:
            dict(field_name=field_value, ...)
        """

        # return dict(self.__transform_response(data))
        return data

    @property
    def __location__(self):
        raise NotImplementedError
