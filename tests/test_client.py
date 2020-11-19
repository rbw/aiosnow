import aiohttp
import pytest

from aiosnow.client import Client
from aiosnow.config import ConfigSchema
from aiosnow.exceptions import (
    AmbiguousClientAuthentication,
    MissingClientAuthentication,
)


def test_client_config_schema_missing_auth():
    """No passing of authentication method to Client should raise ConfigurationException"""

    with pytest.raises(MissingClientAuthentication):
        ConfigSchema(many=False).load(
            dict(address="test", session=dict(use_ssl=True, verify_ssl=True,))
        )


def test_client_config_schema_ambiguous_auth():
    """No passing of authentication method to Client should raise ConfigurationException"""

    with pytest.raises(AmbiguousClientAuthentication):
        ConfigSchema(many=False).load(
            dict(
                address="test",
                session=dict(
                    basic_auth=("username", "password"),
                    oauth={},
                    use_ssl=True,
                    verify_ssl=True,
                ),
            )
        )


def test_client_config_schema_common():
    """No passing of authentication method to Client should raise ConfigurationException"""

    config = ConfigSchema(many=False).load(
        dict(
            address="test",
            session=dict(
                basic_auth=("username", "password"), use_ssl=True, verify_ssl=True,
            ),
        )
    )

    assert config.address == "test"
    assert config.session.basic_auth == ("username", "password")
    assert config.session.use_ssl is True
    assert config.session.verify_ssl is True


def test_client_config_full():
    """Client config should load into a config object"""

    config = dict(
        address="test.service-now.com",
        basic_auth=("test", "test"),
        use_ssl=True,
        verify_ssl=True,
    )

    client = Client(**config)

    assert client.config.address == config["address"]
    assert client.config.session.basic_auth == config["basic_auth"]
    assert client.config.session.use_ssl == config["use_ssl"]
    assert client.config.session.verify_ssl == config["verify_ssl"]


async def test_client_get_session():
    """Client session factory should produce a aiosnow.client.Session object"""

    client = Client("test.service-now.com", basic_auth=("test", "test"))
    session = client.get_session()

    assert isinstance(session, aiohttp.ClientSession)
    assert isinstance(client._auth, aiohttp.helpers.BasicAuth)
