import warnings
from typing import Any, Iterable, Tuple, Union

import marshmallow

from aiosnow.exceptions import (
    IncompatiblePayloadField,
    UnexpectedPayloadType,
    UnknownPayloadField,
)

from .fields.base import BaseField
from .fields.mapped import MappedField


class BaseSchemaMeta(marshmallow.schema.SchemaMeta):
    def __new__(mcs, name: str, bases: tuple, attrs: dict) -> Any:
        fields = getattr(bases[0], "_declared_fields", {})  # Inherit from parent
        fields.update(getattr(mcs, "_declared_fields", {}))  # Merge

        for key, value in attrs.items():
            if isinstance(value, BaseField):
                fields[key] = value
                fields[key].name = key
            elif isinstance(value, BaseSchemaMeta):
                fields[key] = Nested(key, value, allow_none=True, required=False)

        attrs["fields"] = fields
        cls = super().__new__(mcs, name, bases, attrs)

        for name, field in fields.items():
            setattr(cls, name, field)

        return cls


class Nested(marshmallow.fields.Nested):
    def __init__(self, parent_name: str, nested_cls: type, *args: Any, **kwargs: Any):
        fields = getattr(nested_cls, "_declared_fields", {})

        for name, field in fields.items():
            field.name = f"{parent_name}.{name}"
            setattr(self, name, field)

        super(Nested, self).__init__(nested_cls, *args, **kwargs)


class BaseSchema(marshmallow.Schema, metaclass=BaseSchemaMeta):
    """Abstract base schema

    Attributes:
        nested_fields (list): List of nested field names
    """

    class Meta:
        pass

    aiosnow_meta: Any = None

    def __init__(self, *args: Any, **kwargs: Any):
        self.nested_fields = {
            n: f for n, f in self.fields.items() if isinstance(f, Nested)
        }
        super(BaseSchema, self).__init__(*args, **kwargs)

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
            field = self.fields.get(key, None)

            if not field:
                warnings.warn(
                    f"Unexpected field in response content: {key}, skipping..."
                )
                continue

            if isinstance(field, BaseField):
                if isinstance(value, dict) and {"value", "display_value"} <= set(
                    value.keys()
                ):
                    if isinstance(field, MappedField):
                        value = value["value"] or None, value["display_value"] or None
                    else:
                        value = value[field.pluck.value] or None
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
            many: Whether to serialize `obj` as a collection. If `None`, the value for `self.many` is used.

        Returns:
            JSON string
        """

        if not isinstance(obj, dict):
            raise UnexpectedPayloadType(
                f"Invalid payload: {type(obj)}, expected: {dict}"
            )

        data = dict(self.__dump_payload(obj))
        return super().dumps(data)
