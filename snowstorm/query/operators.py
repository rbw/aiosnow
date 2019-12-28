class ConditionalBase:
    EQUALS = "="
    NOT_EQUALS = "!="
    LESS = "<"
    LESS_EQUAL = "<="
    GREATER = ">"
    GREATER_EQUAL = ">="
    CONTAINS = "*"
    NOT_CONTAINS = "!*"
    EMPTY = "ISEMPTY"
    POPULATED = "ISNOTEMPTY"
    SAME = "SAMEAS"
    DIFFERENT = "NSAMEAS"
    BETWEEN = "BETWEEN"


class String(ConditionalBase):
    EMPTYSTRING = "EMPTYSTRING"
    STARTSWITH = "STARTSWITH"
    ENDSWITH = "ENDSWITH"
    ANYTHING = "ANYTHING"


class Reference(ConditionalBase):
    EMPTYSTRING = "EMPTYSTRING"


class Numeric(ConditionalBase):
    RELATED_GREATER = "GT_FIELD"
    RELATED_LESS = "LT_FIELD"
    RELATED_GREATER_EQUALS = "GT_OR_EQUALS_FIELD"
    RELATED_LESS_EQUALS = "LE_OR_EQUALS_FIELD"


class Choice:
    ONEOF = "IN"
    NOTONEOF = "NOT IN"


class ChoiceNumeric(Choice, Numeric):
    pass


class ChoiceString(Choice, String):
    pass


class DateTime(ConditionalBase):
    TODAY = "ONToday"
    NOT_TODAY = "NOTONToday"
    TREND = "DATEPART"
    RELATIVE_GREATER = "RELATIVEGE"
    RELATIVE_LESS = "RELATIVELE"
    RELATIVE_EQUALS = "RELATIVEEE"
    RELATED_GREATER = "MORETHAN"
    RELATED_LESS = "LESSTHAN"


class Boolean(ConditionalBase):
    pass


class EmailNotification:
    CHANGES = "VALCHANGES"
    CHANGES_FROM = "CHANGESFROM"
    CHANGES_TO = "CHANGESTO"


class Logical:
    AND = "^"
    OR = "^OR"
    NQ = "^NQ"
