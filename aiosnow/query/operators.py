class BaseOperator:
    EQUALS = "="
    NOT_EQUALS = "!="
    LESS = "<"
    LESS_EQUALS = "<="
    GREATER = ">"
    GREATER_EQUALS = ">="
    CONTAINS = "*"
    NOT_CONTAINS = "!*"
    EMPTY = "ISEMPTY"
    POPULATED = "ISNOTEMPTY"
    BETWEEN = "BETWEEN"
    ANYTHING = "ANYTHING"
    SAME = "SAMEAS"
    DIFFERENT = "NSAMEAS"
    ONEOF = "IN"
    NOT_ONEOF = "NOT IN"


class StringOperator(BaseOperator):
    EMPTYSTRING = "EMPTYSTRING"
    STARTSWITH = "STARTSWITH"
    ENDSWITH = "ENDSWITH"


class ReferenceField(StringOperator):
    pass


class IntegerOperator(BaseOperator):
    class Related:
        GREATER = "GT_FIELD"
        LESS = "LT_FIELD"
        GREATER_EQUALS = "GT_OR_EQUALS_FIELD"
        LESS_EQUALS = "LE_OR_EQUALS_FIELD"


class DateTimeOperator(BaseOperator):
    ON = "ON"
    NOT_ON = "NOTON"
    TREND = "DATEPART"
    RELATIVE_GREATER = "RELATIVEGE"
    RELATIVE_LESS = "RELATIVELE"
    RELATIVE_EQUALS = "RELATIVEEE"
    RELATED_GREATER = "MORETHAN"
    RELATED_LESS = "LESSTHAN"


class BooleanOperator(BaseOperator):
    pass


class EmailOperator:
    CHANGES = "VALCHANGES"
    CHANGES_FROM = "CHANGESFROM"
    CHANGES_TO = "CHANGESTO"


class LogicalOperator:
    AND = "^"
    OR = "^OR"
    NQ = "^NQ"
