from .resource import Resource, Schema, QueryBuilder, select
from .consts import Joined


class Snowstorm:
    def __init__(self, config):
        self.config = config

    def resource(self, schema) -> Resource:
        return Resource(schema, self.config)
