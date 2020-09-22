from __future__ import annotations

from typing import Any, List

from aiosnow.consts import SORT_ASCENDING, SORT_DESCENDING

from .condition import Condition


class QueryBuilder:
    sysparms: str = ""

    @classmethod
    def produce_builder(cls, sysparms: str) -> QueryBuilder:
        builder = cls()
        builder.sysparms = sysparms
        return builder

    @classmethod
    def from_chain(cls, items: List[Condition]) -> QueryBuilder:
        sysparms = "".join([str(i) for i in items])
        return cls.produce_builder(sysparms)

    @classmethod
    def from_raw(cls, sysparms: str) -> QueryBuilder:
        return cls.produce_builder(sysparms)

    def _order_by(self, value: Any, ascending: bool = True) -> str:
        items = value if isinstance(value, list) else [value]
        sort = SORT_ASCENDING if ascending else SORT_DESCENDING
        sort_statements = []
        for value in items:
            if hasattr(value, "name"):
                name = f"{value.name}"
            else:
                name = f"{value}"

            sort_statements.append(sort + name)

        prefix = "^" if self.sysparms else ""
        return prefix + "^".join(sort_statements)

    def order_desc(self, value: Any) -> QueryBuilder:
        self.sysparms += self._order_by(value, ascending=False)
        return self

    def order_asc(self, value: Any) -> QueryBuilder:
        self.sysparms += self._order_by(value)
        return self

    def __repr__(self) -> Any:
        return self.sysparms
