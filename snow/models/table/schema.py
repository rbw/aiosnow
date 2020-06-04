from typing import Any

from snow.model.schema.base import BaseSchema, BaseSchemaMeta


class TableSchemaMeta(BaseSchemaMeta):
    def __new__(mcs, name: str, bases: tuple, attrs: dict) -> Any:
        base_cls = bases[0]
        cls = super().__new__(mcs, name, bases, attrs)

        table_name = hasattr(cls.Meta, "table_name") and cls.Meta.table_name or None

        if not table_name and hasattr(base_cls, "Meta"):
            table_name = (
                hasattr(base_cls.Meta, "table_name")
                and base_cls.Meta.table_name
                or None
            )

        cls.snow_meta = type(
            "Meta",
            (),
            dict(
                table_name=table_name,
                return_only=hasattr(cls.Meta, "return_only")
                and cls.Meta.return_only
                or None,
            ),
        )()

        return cls


class TableSchema(BaseSchema, metaclass=TableSchemaMeta):
    """TableSchema

    Describes TableModel

    Attributes:
        snow_meta: Schema config object
    """

    class Meta:
        """Meta config object"""

        @property
        def table_name(self) -> str:
            """Table name"""
            raise NotImplementedError

        @property
        def return_only(self) -> list:
            """Return only these fields"""
            raise NotImplementedError

    snow_meta: Meta
