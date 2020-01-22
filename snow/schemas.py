from collections import namedtuple

from marshmallow import Schema, fields, post_load


class ResponseErrorSchema(Schema):
    message = fields.String()
    detail = fields.String(allow_none=True)


class ConfigSchema(Schema):
    @post_load
    def post_load(self, data, **kwargs):
        Config = namedtuple("Config", self.declared_fields.keys())
        return Config(**data)

    address = fields.String(required=True)
    username = fields.String(required=True)
    password = fields.String(required=True)
