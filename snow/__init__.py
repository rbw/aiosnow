import re
from typing import Type

import aiohttp
from marshmallow import ValidationError

from snow.config import ConfigSchema
from snow.consts import Joined
from snow.exceptions import (
    ConfigurationException,
    IncompatibleSession,
    InvalidSessionType,
    NoAuthenticationMethod,
    UnexpectedSchema,
)
from snow.request.response import Response
from snow.resource import QueryBuilder, Resource, Schema, select
from snow.session import Session


class Application:
    """Snow Application

    The Application class serves a number of purposes:
        - Config validation and transformation
        - Resource factory
        - ClientSession factory

    Args:
        session: Session config dictionary or a Custom snow.Session object

    Attributes:
        config: Application configuration object
    """

    _preconf_session = None

    def __init__(
        self,
        address: str,
        basic_auth: tuple = None,
        use_ssl: bool = True,
        verify_ssl: bool = True,
        session: Session = None,
    ):
        app_config = dict(address=address)

        if session:
            if not isinstance(session, Session):
                raise InvalidSessionType(
                    f"The snow.Application expects session to be a {Session}, not {session}"
                )

            self._preconf_session = session
        else:
            app_config["session"] = dict(
                basic_auth=basic_auth, use_ssl=use_ssl, verify_ssl=verify_ssl
            )

        try:
            self.config = ConfigSchema(many=False).load(app_config)
        except ValidationError as e:
            raise ConfigurationException(e)

    @property
    def _auth(self) -> aiohttp.BasicAuth:
        """Get authentication object built using config

        Returns:
            aiohttp-compatible authentication object
        """

        if self.config.session.basic_auth:
            return aiohttp.BasicAuth(*self.config.session.basic_auth)  # type: ignore
        else:
            raise NoAuthenticationMethod("No known authentication methods was provided")

    def get_session(self) -> Session:
        """New client session

        Returns:
            aiohttp.ClientSession:  HTTP client session

        Raises:
            NoAuthenticationMethod
        """

        if self._preconf_session:
            return self._preconf_session

        connector_args = {}  # type: dict

        if self.config.session.use_ssl:
            connector_args["verify_ssl"] = self.config.session.verify_ssl

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
