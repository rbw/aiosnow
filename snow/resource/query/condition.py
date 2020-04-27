from __future__ import annotations

from typing import Union

from .operators import LogicalOperator


class Condition:
    def __init__(self, key: str, operator: str, value: Union[str, int, None]):
        self.operand_left = key
        self.operand_right = value
        self.operator_conditional = operator
        self.operator_logical = ""
        self.selection = [self]

    @property
    def __str__(self) -> str:
        return (
            (self.operator_logical or "")
            + self.operand_left
            + self.operator_conditional
            + str(self.operand_right)
        )

    def _set_next(self, next_cond: Condition, operator: str) -> Condition:
        next_cond.operator_logical = operator
        self.selection.append(next_cond)
        return self

    def __and__(self, next_cond: Condition) -> Condition:
        return self._set_next(next_cond, LogicalOperator.AND)

    def __or__(self, next_cond: Condition) -> Condition:
        return self._set_next(next_cond, LogicalOperator.OR)

    def __xor__(self, next_cond: Condition) -> Condition:
        return self._set_next(next_cond, LogicalOperator.NQ)
