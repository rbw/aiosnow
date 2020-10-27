from typing import Any, Iterable, Tuple, Union

import marshmallow

from aiosnow.exceptions import (
    DeserializationError,
    IncompatiblePayloadField,
    SchemaError,
    SerializationError,
    UnexpectedPayloadType,
    UnknownPayloadField,
)

from .fields.base import BaseField
from .fields.mapped import MappedField
from .nested import Nested


class ModelSchemaMeta(marshmallow.schema.SchemaMeta):
    def __new__(mcs, name: str, bases: tuple, attrs: dict) -> Any:
        fields = attrs["fields"] = {}
        nested_fields = attrs["nested_fields"] = {}
        pks = []

        for k, v in attrs.items():
            if isinstance(v, BaseField):
                if v.is_primary:
                    pks.append(k)

                fields[k] = v
                fields[k].name = k
            elif isinstance(v, ModelSchemaMeta):
                fields[k] = Nested(k, v, allow_none=True, required=False)
                nested_fields.update({k: fields[k]})
            else:
                continue

        if len(pks) == 1:
            attrs["_primary_key"] = pks[0]
        elif len(pks) == 0:
            attrs["_primary_key"] = None
        elif len(pks) > 1:
            raise SchemaError(
                f"Multiple primary keys (is_primary) supplied "
                f"in {name}. Maximum allowed is 1."
            )

        cls = super().__new__(mcs, name, bases, {**attrs, **fields})

        for k, v in fields.items():
            setattr(cls, k, v)

        return cls


class ModelSchema(marshmallow.Schema, metaclass=ModelSchemaMeta):
    @marshmallow.pre_load
    def _load_response(self, data: Union[list, dict], **_: Any) -> Union[list, dict]:
        """Load response content
        @TODO - move into load()

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
            field = self._declared_fields.get(key, None)

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

    def load_content(self, *args: Any, **kwargs: Any) -> dict:
        try:
            return self._do_load(*args, partial=True, postprocess=True, **kwargs)
        except marshmallow.exceptions.ValidationError as e:
            raise DeserializationError(e)

    def loads(self, *args: Any, **kwargs: Any) -> dict:
        try:
            return super().loads(*args, **kwargs)
        except marshmallow.exceptions.ValidationError as e:
            raise DeserializationError(e)

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

        try:
            return super().dumps(data)
        except marshmallow.exceptions.ValidationError as e:
            raise SerializationError(e)
