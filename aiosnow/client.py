from typing import Dict, Union

import aiohttp
from marshmallow import ValidationError

from aiosnow.config import ConfigSchema
from aiosnow.exceptions import (
    ConfigurationError,
    IncompatibleSession,
    NoAuthenticationMethod,
)
from aiosnow.request import Response
from aiosnow.session import Session
from aiosnow.utils import get_url


class Client:
    """aiosnow client

    Args:
        address: Instance TCP address, example: my-instance.service-now.com
        basic_auth: Tuple of (username, password)
        use_ssl: Whether to use SSL
        verify_ssl: Whether to verify SSL certificates
        session: Custom aiohttp.ClientSession object

    Attributes:
        config: Client configuration object
    """

    _preconf_session = None

    def __init__(
        self,
        address: Union[str, bytes],
        basic_auth: tuple = None,
        use_ssl: bool = True,
        verify_ssl: bool = None,
        session: aiohttp.ClientSession = None,
    ):
        app_config: Dict = dict(address=address)

        if session:
            if not isinstance(session, aiohttp.ClientSession):
                raise IncompatibleSession(
                    f"The aiosnow.Client expects :session: to be a aiosnow-compatible "
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
                raise ConfigurationError(
                    f"Client Session factory configuration params {session_config_params} "
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
            raise ConfigurationError(e)

        self.base_url = get_url(str(self.config.address), bool(use_ssl))

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
