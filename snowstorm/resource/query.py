_registry = []


class QueryBuilder:
    def __init__(self, key):
        self.key = key
        self.value = None
        self.segment = []

    def __and__(self, other):
        self.segment.extend(["^", other.key])
        return other

    def __or__(self, other):
        self.segment.extend(["^OR", other.key])
        return other

    def eq(self, other):
        self.segment.extend([other])
        _registry.append(self.segment)
        print(_registry)
        return self
