import aiohttp

from marshmallow import ValidationError

from .resource import Resource, Schema, QueryBuilder, select
from .consts import Joined
from .config import Config
from .exceptions import ConfigurationException


class Application:
    """Validates the config and provides a factory for producing resources

    Args:
        address (str): Instance address, e.g. https://my_instance.service-now.com
        basic_auth (tuple): (<username>, <password>)

    Attributes:
        config: config dictionary
    """

    def __init__(self, **config_data):
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

    def resource(self, schema) -> Resource:
        """Snow Resource factory

        Args:
            schema: Resource Schema

        Returns:
            Resource
        """
        return Resource(schema, self)
