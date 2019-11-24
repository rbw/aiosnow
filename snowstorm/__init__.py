from .resource import Resource, Schema, fields


class Snowstorm:
    def __init__(self, config):
        self.config = config

    def resource(self, schema):
        return Resource(schema, self.config)
