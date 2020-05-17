import warnings
from typing import Any, Iterable, Tuple, Union

import marshmallow

from snow.exceptions import (
    IncompatiblePayloadField,
    NoSchemaFields,
    UnexpectedPayloadType,
    UnknownPayloadField,
)

from .fields import BaseField


class SchemaMeta(marshmallow.schema.SchemaMeta):
    def __new__(mcs, name: str, bases: tuple, attrs: dict) -> Any:
        base_cls = bases[0]
        fields = getattr(base_cls, "_declared_fields", {})

        for key, value in attrs.items():
            if isinstance(value, BaseField):
                fields[key] = value
            elif isinstance(value, SchemaMeta):
                fields[key] = Nested(key, value, allow_none=True, required=False)

        attrs.update(fields)
        cls = super().__new__(mcs, name, bases, attrs)

        for name, field in fields.items():
            if not isinstance(field, Nested):
                field.name = name

            setattr(cls, name, field)

        if hasattr(cls, "snow_meta"):
            location = (
                hasattr(cls.Meta, "location") and getattr(cls.Meta, "location") or None
            )

            if not location and hasattr(base_cls, "Meta"):
                location = (
                    hasattr(base_cls.Meta, "location")
                    and base_cls.Meta.location
                    or None
                )

            if isinstance(location, str):
                cls.snow_meta = type("Meta", (), dict(location=location))

        return cls


class Nested(marshmallow.fields.Nested):
    def __init__(self, parent_name: str, nested_cls: type, *args: Any, **kwargs: Any):
        for name, field in getattr(nested_cls, "_declared_fields").items():
            field.name = f"{parent_name}.{name}"
            setattr(self, name, field)

        super(Nested, self).__init__(nested_cls, *args, **kwargs)


class Schema(marshmallow.Schema, metaclass=SchemaMeta):
    """Resource schema

    Attributes:
        snow_meta: Schema Meta object
    """

    joined_with: str = ""

    class Meta:
        @property
        def location(self) -> str:
            raise NotImplementedError

    snow_meta: Meta = None

    def __init__(self, *args: Any, joined_with: str = None, **kwargs: Any):
        self.snow_fields = self.get_fields()
        self.nested_fields = [
            k for k, v in self.snow_fields.items() if isinstance(v, Nested)
        ]

        if joined_with:
            self.joined_with = joined_with

            # Enable automatic dot-walking of joined fields
            for field in self.snow_fields.values():
                field.name = f"{joined_with}.{field.name}"

        super(Schema, self).__init__(*args, **kwargs)

    @classmethod
    def get_fields(cls) -> dict:
        fields = {}
        for name, field in cls.__dict__.items():
            if name.startswith("_") or name == "opts":
                continue

            fields[name] = field

        if not fields:
            raise NoSchemaFields(f"Schema {cls} lacks fields definitions")

        return fields

    @property
    def _snow_fields(self):
        for name, field in self.__dict__.items():
            if not isinstance(field, (BaseField, SchemaMeta)):
                continue

            yield name, field

    @marshmallow.pre_load
    def _load_response(self, data: Union[list, dict], **_: Any) -> Union[list, dict]:
        """Load response content

        Args:
            data: Dictionary of fields to deserialize

        Returns:
            dict(field_name=field_value, ...)
        """

        if isinstance(data, list):
            return [dict(self.__load_response(r or {})) for r in data]
        elif isinstance(data, dict):
            return dict(self.__load_response(data or {}))
        else:
            raise TypeError(
                f"Response content must be {list} or {dict}, got: {type(data)}"
            )

    def __load_response(self, content: dict) -> Iterable[Tuple[str, str]]:
        """Yields deserialized response content items

        Args:
            content: Response content to deserialize

        Yields: <name>, <value>
        """

        for key, value in content.items():
            field = self.snow_fields.get(key, None)

            if not field:
                warnings.warn(
                    f"Unexpected field in response content: {key}, skipping..."
                )
                continue

            if isinstance(field, BaseField):
                if isinstance(value, str):
                    pass
                elif isinstance(value, dict) and {"value", "display_value"} <= set(
                    value.keys()
                ):
                    value = value[field.joined.value]
            elif isinstance(field, Nested):
                pass
            else:  # Unknown field
                continue

            yield key, value

    def __dump_payload(self, payload: dict) -> Iterable[Tuple[str, str]]:
        """Yields serialized payload

        Args:
            payload: Payload to serialize

        Yields: <name>, <value>
        """

        for key, value in payload.items():
            if isinstance(key, BaseField):
                key = key.name
            elif isinstance(key, str):
                pass
            else:
                raise IncompatiblePayloadField(
                    f"Incompatible field in payload: {type(key)}"
                )

            field = getattr(self, key, None)
            if not field:
                raise UnknownPayloadField(f"Unknown field in payload {key}")

            yield key, value

    def dumps(self, obj: dict, *args: Any, many: bool = None, **kwargs: Any) -> str:
        """Dump payload

        Args:
            obj: The object to serialize
            many: Whether to serialize `obj` as a collection. If `None`, the value
            for `self.many` is used.

        Returns:
            JSON string
        """

        if not isinstance(obj, dict):
            raise UnexpectedPayloadType(
                f"Invalid payload: {type(obj)}, expected: {dict}"
            )

        data = dict(self.__dump_payload(obj))
        return super().dumps(data)


class PartialSchema(Schema):
    class Meta:
        location = None
