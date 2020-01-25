import re

from typing import Type

import aiohttp

from marshmallow import ValidationError

from .resource import Resource, Schema, QueryBuilder, select
from .consts import Joined
from .config import Config
from .exceptions import ConfigurationException, UnexpectedSchema


class Application:
    """Validates the config and provides a factory for producing resources

    Args:
        config_data: Config dictionary

    Attributes:
        config: Application config
    """

    def __init__(self, config_data):
        try:
            self.config = Config().load(config_data)
        except ValidationError as e:
            raise ConfigurationException(e)

        self.secrets = self.config["secrets"]

    def get_session(self):
        secrets = self.secrets["basic"]
        return aiohttp.ClientSession(
            auth=aiohttp.helpers.BasicAuth(secrets["username"], secrets["password"]),
        )

    def resource(self, schema: Type[Schema]) -> Resource:
        """Snow Resource factory

        Args:
            schema (Schema): Resource Schema

        Returns:
            Resource: Resource object
        """

        if not issubclass(schema, Schema):
            raise UnexpectedSchema(f"Invalid schema class: {schema}, must be of type {Schema}")
        if not re.match(r"^/.*", str(schema.__location__)):
            raise UnexpectedSchema(
                f"Unexpected path in {schema.__name__}.__location__: {schema.__location__}"
            )

        return Resource(schema, self)
