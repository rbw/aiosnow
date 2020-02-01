from marshmallow import Schema, ValidationError, fields, post_load


class ConfigSchema(Schema):
    """Snow config schema

    Attributes:
        address (str): Instance address, e.g. https://my_instance.service-now.com
        basic_auth (tuple): (<username>, <password>), mutually exclusive with other authentication methods
    """

    class InternalConfig:
        """Internal Application config"""

        def __init__(self, **config):
            for k, v in config.items():
                setattr(self, k, v)

    address = fields.Url(required=True)
    basic_auth = fields.Tuple(tuple_fields=(fields.String(), fields.String()), required=False)

    def __init__(self, *args, **kwargs):
        super(ConfigSchema, self).__init__(*args, **kwargs)

    @post_load
    def make_object(self, data, **_):
        if {"basic_auth", "oauth"} <= set(data):
            raise ValidationError("Cannot use multiple authentication methods")
        elif "basic_auth" in data:
            pass
        else:
            raise ValidationError("No supported authentication method provided")

        return ConfigSchema.InternalConfig(**data)
