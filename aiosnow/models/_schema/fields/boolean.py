import marshmallow

from aiosnow.query import BooleanQueryable

from .base import BaseField


class Boolean(marshmallow.fields.Boolean, BaseField, BooleanQueryable):
    pass
