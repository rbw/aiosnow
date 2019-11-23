from enum import Enum
from collections import namedtuple

import ijson

from ijson.common import ObjectBuilder
from urllib.parse import urlencode, parse_qs


class Condition(Enum):
    SUCCESS = "result"
    FAILURE = "error"


class Structure(Enum):
    ONE = "start_map"
    MANY = "start_array"


State = namedtuple("State", ["condition", "structure"])


class StreamParser:
    structure_type = None
    state = None

    def __init__(self, stream, buf_size=2048):
        self.count = 0
        self.__stream = stream
        self._buf_size = buf_size
        self._builder = ObjectBuilder()

    @property
    def _stream(self):
        for chunk in self.__stream:
            yield chunk

    def handle_event(self, prefix, event, value):
        if (prefix, event) == ("result.item", "end_map"):
            self._builder.event(event, value)
            self.count += 1
            yield getattr(self._builder, "value")
        elif prefix.startswith("result.item"):
            self._builder.event(event, value)

    """def yield_one(self):
        if (prefix, event) == ("result", "end_map"):
            # Reached end of the result object. Set count and yield.
            builder.event(event, value)
            self.count += 1
            yield getattr(builder, "value")
        elif prefix.startswith("result"):
            # Build the error object
            builder.event(event, value)"""

    def parse(self):
        for prefix, event, value in ijson.parse(self):
            if prefix == Condition.SUCCESS.value:
                if Structure.ONE.value in event:
                    self.state = State(Condition.SUCCESS, Structure.ONE)
                elif Structure.MANY.value in event:
                    self.state = State(Condition.SUCCESS, Structure.MANY)
            if prefix == Condition.ERROR.value:
                self.state = State(Condition.FAILURE, Structure.ONE)
            else:
                raise RuntimeError("Invalid response received. Cannot parse stream: [first 10 bytes]")

        print(self.state)
