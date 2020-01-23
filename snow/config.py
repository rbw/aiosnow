from collections import namedtuple

from marshmallow import Schema, ValidationError, fields, post_load, pre_load


class ConfigBase(Schema):
    def __init__(self, *args, **kwargs):
        super(ConfigBase, self).__init__(*args, **kwargs)


class ConfigBasicSecret(ConfigBase):
    """Basic credentials schema

    Attributes:
        username: Authentication username
        password: Authentication password
    """

    username = fields.String(required=True)
    password = fields.String(required=True)


class ConfigSecrets(ConfigBase):
    """Schema for storing secrets

    Attributes:
        basic (ConfigBasicSecret): Basic credentials
    """

    basic = fields.Nested(ConfigBasicSecret)


class Config(ConfigBase):
    """Main configuration schema

    Attributes:
        address: Instance address
        secrets (ConfigSecrets): Authentication secrets
    """

    @pre_load
    def transform(self, data, **_):
        if {"basic_auth", "oauth"} <= set(data):
            raise ValidationError("Cannot use multiple authentication methods")
        elif "basic_auth" in data:
            if not isinstance(data["basic_auth"], tuple):
                raise ValidationError("basic_auth must be a tuple: (<username>, <password>)")

            data["username"], data["password"] = data.pop("credentials")
        else:
            raise ValidationError("No authentication methods were provided")

        return data

    @post_load
    def objectify(self, data, **_):
        for k, v in self.declared_fields.items():
            Config = namedtuple("Config", self.declared_fields.keys())

        return Config(**data)

    address = fields.Url(required=True)
    secrets = fields.Nested(ConfigSecrets)

