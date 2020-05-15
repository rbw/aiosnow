import re
from typing import Dict, Type

import aiohttp
from marshmallow import ValidationError

from snow.config import ConfigSchema
from snow.consts import Joined
from snow.exceptions import (
    ConfigurationException,
    IncompatibleSession,
    NoAuthenticationMethod,
    NoSchemaLocation,
    UnexpectedSchema,
)
from snow.request import Response
from snow.resource import QueryBuilder, Resource, Schema, select
from snow.session import Session


class Application:
    """Snow Application

    The Application class serves a number of purposes:
        - Config validation and transformation
        - Resource factory
        - ClientSession factory

    Args:
        address: Instance TCP address, example: my-instance.service-now.com
        basic_auth: Tuple of (username, password)
        use_ssl: Whether to use SSL
        verify_ssl: Whether to verify SSL certificates
        session: Custom aiohttp.ClientSession object

    Attributes:
        config: Application configuration object
    """

    _preconf_session = None

    def __init__(
        self,
        address: str,
        basic_auth: tuple = None,
        use_ssl: bool = None,
        verify_ssl: bool = None,
        session: aiohttp.ClientSession = None,
    ):
        app_config: Dict = dict(address=address)

        if session:
            if not isinstance(session, aiohttp.ClientSession):
                raise IncompatibleSession(
                    f"The snow.Application expects :session: to be a Snow-compatible "
                    f"{aiohttp.ClientSession}, not {session}"
                )

            resp_cls = getattr(session, "_response_class")
            if resp_cls != Response:
                raise IncompatibleSession(
                    f"The {session} passed to {self} must have its :response_class: "
                    f"set to {Response}, not {resp_cls}"
                )

            session_config_params = [basic_auth, use_ssl, verify_ssl]
            if any([p is not None for p in session_config_params]):
                raise ConfigurationException(
                    f"Application Session factory configuration params {session_config_params} "
                    f"cannot be used with a custom Session object."
                )

            self._preconf_session = session
        else:
            app_config["session"] = dict(
                basic_auth=basic_auth,
                use_ssl=use_ssl or True,
                verify_ssl=verify_ssl or True,
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

    def get_session(self) -> aiohttp.ClientSession:
        """New client session

        Returns:
            aiohttp.ClientSession:  HTTP client session

        Raises:
            NoAuthenticationMethod
        """

        if self._preconf_session:
            return self._preconf_session

        connector_args: dict = {}

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

        try:
            location = schema.snow_meta.location
        except (NotImplementedError, AttributeError):
            raise NoSchemaLocation(f"The {schema.__name__}.Meta.location attribute must be set")

        if not re.match(r"^/.*", location):
            raise UnexpectedSchema(
                f"Unexpected path in {schema.__name__}.Meta.location: {location}"
            )

        return Resource(schema, self)
