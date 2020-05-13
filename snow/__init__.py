import re
from typing import Type

import aiohttp
from marshmallow import ValidationError

from .config import ConfigSchema
from .consts import Joined
from .exceptions import ConfigurationException, NoAuthenticationMethod, UnexpectedSchema
from .request.response import Response
from .resource import QueryBuilder, Resource, Schema, select
from .session import Session


def load_config(config_data: dict) -> ConfigSchema:
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
        config: Application configuration object
    """

    def __init__(self, config_data: dict):
        try:
            self.config = load_config(config_data)
        except ValidationError as e:
            raise ConfigurationException(e)

    @property
    def _auth(self) -> aiohttp.BasicAuth:
        """Get authentication object built using config

        Returns:
            aiohttp-compatible authentication object
        """

        if self.config.basic_auth:
            return aiohttp.BasicAuth(*self.config.basic_auth)  # type: ignore
        else:
            raise NoAuthenticationMethod("No known authentication methods was provided")

    def get_session(self) -> Session:
        """New client session

        Returns:
            aiohttp.ClientSession:  HTTP client session

        Raises:
            NoAuthenticationMethod
        """

        connector_args = {}  # type: dict

        if self.config.use_ssl:
            connector_args["verify_ssl"] = self.config.verify_ssl

        return Session(
            auth=self._auth, connector=aiohttp.TCPConnector(**connector_args)
        )

    def resource(self, schema: Type[Schema]) -> Resource:
        """Snow Resource factory

        Args:
            schema: Resource Schema

        Returns:
            Resource: Resource object

        Raises:
            UnexpectedSchema
        """

        if not issubclass(schema, Schema):
            raise UnexpectedSchema(
                f"Invalid schema class: {schema}, must be of type {Schema}"
            )
        if not re.match(r"^/.*", str(schema.__location__)):
            raise UnexpectedSchema(
                f"Unexpected path in {schema.__name__}.__location__: {schema.__location__}"
            )

        return Resource(schema, self)
