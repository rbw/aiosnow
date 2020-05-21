from enum import Enum

CONTENT_TYPE = "application/json"
SORT_ASCENDING = "ORDERBY"
SORT_DESCENDING = "ORDERBYDESC"


class NestedField(Enum):
    DISPLAY_VALUE = "display_value"
    VALUE = "value"
    LINK = "link"
