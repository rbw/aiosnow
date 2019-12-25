from .resource import Resource, Schema


class Snowstorm:
    def __init__(self, config):
        self.config = config

    def resource(self, schema) -> Resource:
        return Resource(schema, self.config)
