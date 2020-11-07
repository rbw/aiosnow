from typing import Any

import marshmallow


class Nested(marshmallow.fields.Nested):
    def __init__(self, parent_name: str, nested_cls: type, *args: Any, **kwargs: Any):
        fields = getattr(nested_cls, "_declared_fields", {})

        for name, field in fields.items():
            field.name = f"{parent_name}.{name}"
            setattr(self, name, field)

        super(Nested, self).__init__(nested_cls, *args, **kwargs)
