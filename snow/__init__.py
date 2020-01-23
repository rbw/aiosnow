from marshmallow import ValidationError

from .resource import Resource, Schema, QueryBuilder, select
from .consts import Joined
from .config import Config
from .exceptions import ConfigurationException


def config_load(data) -> Config:
    return Config().load(data)


class Application:
    """Validates the config and provides a factory for producing resources

    Args:
        address (str): Instance address, e.g. https://my_instance.service-now.com
        basic_auth (tuple): (<username>, <password>)

    Attributes:
        config (snow.schemas.ConfigSchema): config object
    """

    def __init__(self, **config_data):
        try:
            self.config = config_load(config_data)
        except ValidationError as e:
            raise ConfigurationException(e)

    def resource(self, schema) -> Resource:
        """Snow Resource factory

        Args:
            schema: Resource Schema

        """
        return Resource(schema, self.config)
