from snow.consts import SORT_ASCENDING, SORT_DESCENDING


class QueryBuilder:
    sysparms = None

    @classmethod
    def produce_builder(cls, sysparms):
        builder = cls()
        builder.sysparms = sysparms
        return builder

    @classmethod
    def from_segments(cls, items):
        sysparms = "".join([i.__str__ for i in items])
        return cls.produce_builder(sysparms)

    @classmethod
    def from_raw(cls, sysparms):
        return cls.produce_builder(sysparms)

    def _order_by(self, value, ascending=True):
        items = value if isinstance(value, list) else [value]
        sort = SORT_ASCENDING if ascending else SORT_DESCENDING

        prefix = "^" if self.sysparms else ""
        return prefix + "^".join([f"{sort}{item.name}" for item in items])

    def order_desc(self, value):
        self.sysparms += self._order_by(value, ascending=False)
        return self

    def order_asc(self, value):
        self.sysparms += self._order_by(value)
        return self

    def __repr__(self):
        return self.sysparms
