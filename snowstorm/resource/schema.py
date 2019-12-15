import marshmallow
import ujson


class SchemaOpts(marshmallow.schema.SchemaOpts):
    def __init__(self, meta, **kwargs):
        self.load_only = []
        self.dump_only = []

        super(SchemaOpts, self).__init__(meta, **kwargs)
        self.render_module = ujson
        self.unknown = marshmallow.EXCLUDE


class Schema(marshmallow.Schema):
    OPTIONS_CLASS = SchemaOpts

    @property
    def __location__(self):
        raise NotImplementedError

    __resolve__ = True
