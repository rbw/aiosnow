from marshmallow import ValidationError

from .resource import Resource, Schema, QueryBuilder, select
from .consts import Joined
from .schemas import ConfigSchema
from .exceptions import ConfigurationException


def config_load(config: dict) -> ConfigSchema:
    return ConfigSchema().load(config)


class Client:
    def __init__(self, config: dict):
        """Snow Client

        Args:
            config: config dictionary
        """

        try:
            self.config = config_load(config)
        except ValidationError as e:
            raise ConfigurationException(e)

    def resource(self, schema) -> Resource:
        return Resource(schema, self.config)
