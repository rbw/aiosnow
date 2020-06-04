import warnings
from typing import Any, Dict, Type

import aiohttp
from marshmallow import ValidationError

from snow.config import ConfigSchema
from snow.exceptions import (
    ConfigurationException,
    IncompatibleSession,
    NoAuthenticationMethod,
)
from snow.models.table import TableModel, TableSchema
from snow.request import Response
from snow.session import Session
from snow.utils import get_url


class Snow:
    """Snow Application

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
        use_ssl: bool = True,
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

            session_config_params = [basic_auth, verify_ssl]
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

        self.url = get_url(str(self.config.address), bool(use_ssl))

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
        """

        if self._preconf_session:
            return self._preconf_session

        connector_args: dict = {}

        if self.config.session.use_ssl:
            connector_args["verify_ssl"] = self.config.session.verify_ssl

        return Session(
            auth=self._auth, connector=aiohttp.TCPConnector(**connector_args)
        )

    def resource(self, schema: Type[TableSchema]) -> TableModel:
        warnings.warn(
            "Snow.resource is deprecated, please use Snow.get_table instead",
            DeprecationWarning,
        )
        return self.get_table(schema)

    def get_table(self, schema: Type[TableSchema]) -> TableModel:
        """Snow TableModel factory

        Args:
            schema: TableModel Schema

        Returns:
            Resource: TableModel object
        """

        return TableModel(
            schema,
            instance_url=self.url,
            session=self.get_session(),
            config=self.config,
        )


class Application(Snow):
    def __init__(self, *args: Any, **kwargs: Any):
        warnings.warn(
            "snow.Application is deprecated, please use snow.Snow instead",
            DeprecationWarning,
        )
        super(Application, self).__init__(*args, **kwargs)
