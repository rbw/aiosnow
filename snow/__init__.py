import re

from typing import Type

import aiohttp

from marshmallow import ValidationError

from .resource import Resource, Schema, QueryBuilder, select
from .consts import Joined
from .config import ConfigSchema
from .exceptions import ConfigurationException, UnexpectedSchema, NoAuthenticationMethod


def load_config(config_data):
    return ConfigSchema().load(config_data)


class Application:
    """Snow Application

    The Application class serves a number of purposes:
        - Config validation and transformation
        - Resource factory
        - ClientSession factory

    Args:
        config_data: Config dictionary

    Attributes:
        config (ConfigSchema): Application configuration object
    """

    def __init__(self, config_data):
        try:
            self.config = load_config(config_data)
        except ValidationError as e:
            raise ConfigurationException(e)

    def get_session(self):
        """New client session

        Returns:
            aiohttp.ClientSession:  HTTP client session

        Raises:
            NoAuthenticationMethod
        """

        if self.config.basic_auth:
            return aiohttp.ClientSession(auth=aiohttp.BasicAuth(*self.config.basic_auth))
        else:
            raise NoAuthenticationMethod("No known authentication methods was provided")

    def resource(self, schema: Type[Schema]) -> Resource:
        """Snow Resource factory

        Args:
            schema (Schema): Resource Schema

        Returns:
            Resource: Resource object

        Raises:
            UnexpectedSchema
        """

        if not issubclass(schema, Schema):
            raise UnexpectedSchema(f"Invalid schema class: {schema}, must be of type {Schema}")
        if not re.match(r"^/.*", str(schema.__location__)):
            raise UnexpectedSchema(
                f"Unexpected path in {schema.__name__}.__location__: {schema.__location__}"
            )

        return Resource(schema, self)
