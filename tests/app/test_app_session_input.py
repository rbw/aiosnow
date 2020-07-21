import aiohttp
import pytest

from aiosnow.app import Snow
from aiosnow.exceptions import ConfigurationException, IncompatibleSession
from aiosnow.request.response import Response
from aiosnow.session import Session


def test_app_session_invalid_type():
    """Invalid object type passed to `session` should raise an InvalidSessionType exception"""

    fail_str = dict(address="test.service-now.com", session="test")
    fail_int = dict(address="test.service-now.com", session=123)

    with pytest.raises(IncompatibleSession):
        Snow(**fail_str)
        Snow(**fail_int)


def test_app_session_mutual_exclusive():
    """Passing both a session and session factory configuration should raise ConfigurationException"""

    session = Session()

    with pytest.raises(ConfigurationException):
        Snow("test.service-now.com", session=session, basic_auth=("a", "b"))

    with pytest.raises(ConfigurationException):
        Snow("test.service-now.com", session=session, verify_ssl=True)


def test_app_session_no_auth_method():
    """No authentication method to Application should raise ConfigurationException"""

    with pytest.raises(ConfigurationException):
        Snow("test.service-now.com")


def test_app_session_config_full():
    """Session config should load into a config object"""

    config = dict(
        address="test.service-now.com",
        basic_auth=("test", "test"),
        use_ssl=True,
        verify_ssl=True,
    )

    app = Snow(**config)

    assert app.config.address == config["address"]
    assert app.config.session.basic_auth == config["basic_auth"]
    assert app.config.session.use_ssl == config["use_ssl"]
    assert app.config.session.verify_ssl == config["verify_ssl"]


def test_app_session_object():
    """Compatible user-provided Session objects should be returned from Application.get_session"""

    session = Session()
    app = Snow("test.service-now.com", session=session)
    assert app.get_session() == app._preconf_session == session


def test_app_session_invalid_response_class():
    """Compatible user-provided Session objects should be returned from Application.get_session"""

    session = aiohttp.ClientSession()

    with pytest.raises(IncompatibleSession):
        Snow("test.service-now.com", session=session)


def test_app_session_response_class():
    """Compatible user-provided Session objects should be returned from Application.get_session"""

    session = aiohttp.ClientSession(response_class=Response)
    app = Snow("test.service-now.com", session=session)

    assert app.get_session()._response_class == Response
