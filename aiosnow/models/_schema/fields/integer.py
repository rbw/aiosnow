import marshmallow

from aiosnow.query import IntegerQueryable

from .base import BaseField


class Integer(marshmallow.fields.Integer, BaseField, IntegerQueryable):
    pass
