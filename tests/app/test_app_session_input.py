import pytest

from snow import Application, Session
from snow.exceptions import ConfigurationException, InvalidSessionType


def test_app_session_invalid_type():
    """Invalid object type passed to `session` should raise an InvalidSessionType exception"""

    fail_str = dict(address="test.service-now.com", session="test")
    fail_int = dict(address="test.service-now.com", session=123)

    with pytest.raises(InvalidSessionType):
        Application(**fail_str)
        Application(**fail_int)


def test_app_session_mutual_exclusive():
    """Passing both a session and session factory configuration should raise ConfigurationException"""

    session = Session()

    with pytest.raises(ConfigurationException):
        Application("test.service-now.com", session=session, basic_auth=("a", "b"))

    with pytest.raises(ConfigurationException):
        Application("test.service-now.com", session=session, use_ssl=False)

    with pytest.raises(ConfigurationException):
        Application("test.service-now.com", session=session, verify_ssl=True)


def test_app_session_no_auth_method():
    """No authentication method to Application should raise ConfigurationException"""

    with pytest.raises(ConfigurationException):
        Application("test.service-now.com")


def test_app_session_config_full():
    """Session config should load into a config object"""

    config = dict(
        address="test.service-now.com",
        basic_auth=("test", "test"),
        use_ssl=True,
        verify_ssl=True,
    )

    app = Application(**config)

    assert app.config.address == config["address"]
    assert app.config.session.basic_auth == config["basic_auth"]
    assert app.config.session.use_ssl == config["use_ssl"]
    assert app.config.session.verify_ssl == config["verify_ssl"]


def test_app_session_object():
    """Compatible user-provided Session objects should be returned from Application.get_session"""

    session = Session()
    app = Application("test.service-now.com", session=session)

    assert app.get_session() == session
