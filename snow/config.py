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

    address = fields.Url(required=True)
    secrets = fields.Nested(ConfigSecrets)

    def _basic_secret(self, username, password):
        return dict(
            basic=dict(
                username=username,
                password=password
            )
        )

    @pre_load
    def transform(self, data, **_):
        data["secrets"] = {}

        if {"basic_auth", "oauth"} <= set(data):
            raise ValidationError("Cannot use multiple authentication methods")
        elif "basic_auth" in data:
            credentials = data.pop("basic_auth")
            if not isinstance(credentials, tuple):
                raise ValidationError("basic_auth must be a tuple: (<username>, <password>)")

            secret = self._basic_secret(*credentials)
            data["secrets"].update(secret)
        else:
            raise ValidationError("No authentication method provided")

        return data
