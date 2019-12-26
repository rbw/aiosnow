from .resource import Resource
from .query import QueryBuilder


class Snowstorm:
    def __init__(self, config):
        self.config = config

    def resource(self, schema) -> Resource:
        return Resource(schema, self.config)
