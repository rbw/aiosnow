from __future__ import annotations

import json
from typing import Any

from marshmallow import Schema, ValidationError, fields, post_load

from aiosnow.exceptions import ConfigurationError


class ConfigEncoder(json.JSONEncoder):
    def default(self, o: BaseConfigSchema.ConfigSegment) -> dict:
        return o.as_dict()


class BaseConfigSchema(Schema):
    class ConfigSegment:
        """Internal config segment"""

        def __repr__(self) -> str:
            return json.dumps(self.__config, cls=ConfigEncoder, indent=4)

        def as_dict(self) -> dict:
            return self.__config

        def __init__(self, **config: dict):
            self.__config = config
            for k, v in config.items():
                setattr(self, k, v)

    @post_load
    def make_object(self, data: dict, **_: Any) -> Any:
        try:
            return self.ConfigSegment(**data)
        except ValidationError as exc:
            raise ConfigurationError from exc


class SessionConfig(BaseConfigSchema):
    """Session config schema

    Attributes:
        address (str): Instance address, e.g. my_instance.service-now.com
        basic_auth (tuple): (<username>, <password>), mutually exclusive with other authentication methods
        use_ssl (bool): Whether to use SSL, defaults to True
        verify_ssl (bool): Whether to validate SSL certificates, defaults to True
    """

    def __init__(self, *args: Any, **kwargs: Any):
        super(SessionConfig, self).__init__(*args, **kwargs)

    basic_auth = fields.Tuple(
        tuple_fields=(fields.String(), fields.String()), required=False, allow_none=True
    )
    use_ssl = fields.Boolean(missing=True)
    verify_ssl = fields.Boolean(missing=True)

    @post_load
    def make_object(self, data: dict, **_: Any) -> Any:
        if {"basic_auth", "oauth"} <= set(data):
            raise ValidationError("Cannot use multiple authentication methods")
        elif data.get("basic_auth"):
            pass
        else:
            raise ValidationError("No supported authentication method provided")

        return super().make_object(data)


class ConfigSchema(BaseConfigSchema):
    """Aiosnow config schema

    Attributes:
        session (bool): Session config
    """

    address = fields.String(required=True)
    session = fields.Nested(
        SessionConfig, default={}, allow_none=True
    )  # type: SessionConfig # type: ignore

    def __init__(self, *args: Any, **kwargs: Any):
        super(ConfigSchema, self).__init__(*args, **kwargs)

    def load(self, *args: Any, **kwargs: Any) -> ConfigSchema:
        return super().load(*args, **kwargs)
