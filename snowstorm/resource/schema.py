import marshmallow
import ujson


class JsonSerializer:
    @staticmethod
    def loads(data, **kwargs):
        return ujson.loads(data, **kwargs)

    @staticmethod
    def dumps(data, **kwargs):
        return ujson.dumps(data, **kwargs)


class SchemaOpts(marshmallow.schema.SchemaOpts):
    def __init__(self, meta, **kwargs):
        self.load_only = []
        self.dump_only = []

        super(SchemaOpts, self).__init__(meta, **kwargs)
        self.render_module = JsonSerializer
        self.unknown = marshmallow.EXCLUDE


class ResourceSchema(marshmallow.Schema):
    OPTIONS_CLASS = SchemaOpts

    __location__ = None
