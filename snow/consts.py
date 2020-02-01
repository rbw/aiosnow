from enum import Enum

CONTENT_TYPE = "application/json"
SORT_ASCENDING = "ORDERBY"
SORT_DESCENDING = "ORDERBYDESC"


class Joined(Enum):
    """Pluck-targets of "joined" fields"""

    DISPLAY_VALUE = "display_value"
    VALUE = "value"
    LINK = "link"
