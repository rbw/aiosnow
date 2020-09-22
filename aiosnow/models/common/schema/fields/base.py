from typing import Any

import marshmallow

from aiosnow.models.common.schema.helpers import Pluck


class BaseField(marshmallow.fields.Field):
    def __init__(
        self,
        *args: Any,
        pluck: Pluck = Pluck.VALUE,
        is_primary: bool = False,
        **kwargs: Any,
    ):
        self.pluck = Pluck(pluck)
        self.is_primary = is_primary
        super(BaseField, self).__init__(*args, **kwargs)
        self.allow_none = True
        self.missing = None

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} [maps_to={self.pluck}, primary={self.is_primary}]>"
