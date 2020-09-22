import marshmallow

from aiosnow.query import DateTimeQueryable

from .base import BaseField


class DateTime(marshmallow.fields.DateTime, BaseField, DateTimeQueryable):
    def _bind_to_schema(self, field_name: str, schema: marshmallow.Schema) -> None:
        """Removing this override causes marshmallow schema-field registration to fail
        because self.root resolves to None when inheriting schemas? This
        seems exclusive to the DateTime type, and could be a marshmallow bug.

        "AttributeError: 'NoneType' object has no attribute 'opts'"

        @TODO - find out why DateTime schema parent fails to resolve for DateTime and remove this override"""

        self.format = (
            self.format
            or getattr(schema.opts, self.SCHEMA_OPTS_VAR_NAME)
            or self.DEFAULT_FORMAT
        )
