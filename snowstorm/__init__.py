from .resource import Resource, Schema
from .query import QueryBuilder
from .consts import Target


class Snowstorm:
    def __init__(self, config):
        self.config = config

    def resource(self, schema) -> Resource:
        return Resource(schema, self.config)
