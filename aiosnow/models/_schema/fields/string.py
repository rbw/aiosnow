import marshmallow

from aiosnow.query import StringQueryable

from .base import BaseField


class String(marshmallow.fields.String, BaseField, StringQueryable):
    pass
