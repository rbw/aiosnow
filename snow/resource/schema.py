import warnings
from typing import Any, Dict, Iterable, Optional, Tuple, Union

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
        fields = {}  # type: Dict[Any, Union[BaseField, Nested]]

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
    def __init__(self, parent_name: str, nested_cls: type, *args: Any, **kwargs: Any):
        for name, field in getattr(nested_cls, "_declared_fields").items():
            field.name = f"{parent_name}.{name}"
            setattr(self, name, field)

        super(Nested, self).__init__(nested_cls, *args, **kwargs)


class Schema(marshmallow.Schema, metaclass=SchemaMeta):
    """Resource schema

    Attributes:
        __location__: API path
    """

    joined_with: str = ""

    def __init__(self, *args: Any, joined_with: str = None, **kwargs: Any):
        self.registered_fields = self.get_fields()
        self.nested_fields = [
            k for k, v in self.registered_fields.items() if isinstance(v, Nested)
        ]

        if joined_with:
            self.joined_with = joined_with

            # Enable automatic dot-walking of joined fields
            for field in self.get_fields().values():
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

    def __load_response(self, content: dict) -> Iterable[Tuple[str, str]]:
        """Yields deserialized response content items

        Args:
            content: Response content to deserialize

        Yields: <name>, <value>
        """

        for key, value in content.items():
            field = self.registered_fields.get(key, None)

            if isinstance(field, BaseField):
                if isinstance(value, str):
                    pass
                elif isinstance(value, dict) and {"value", "display_value"} <= set(
                    value.keys()
                ):
                    if not field.name or not getattr(self, field.name, None):
                        warnings.warn(
                            f"Unexpected field in response content: {field.name}, skipping..."
                        )
                        continue

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
            raise TypeError(f"Response content must be {list} or {dict}, got: {type(data)}")

    @property
    def __location__(self) -> Optional[str]:
        raise NotImplementedError


class PartialSchema(Schema):
    @property
    def __location__(self) -> None:
        return
