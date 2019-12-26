from enum import Enum


class StringOperator(Enum):
    EQUALS = "="


class LogicalOperator(Enum):
    AND = "^"
    OR = "^OR"
    NQ = "^NQ"
