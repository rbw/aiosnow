from snowstorm.exceptions import InvalidSegment
from .segment import Segment


class QueryBuilder:
    def __init__(self, root):
        if not isinstance(root, Segment):
            raise InvalidSegment(f"Invalid segment for f{self}: {root}, expected: {Segment}")

        self.conditions = root.instances

    def __repr__(self):
        return self.sysparms

    @property
    def sysparms(self):
        return "".join([c.__str__ for c in self.conditions])

