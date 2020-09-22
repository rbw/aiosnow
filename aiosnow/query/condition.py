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

    def __str__(self) -> str:
        """Condition string representation

        Returns: ServiceNow sysparm string
        """

        return (
            (self.operator_logical or "")
            + self.operand_left
            + self.operator_conditional
            + str(self.operand_right)
        )

    def _set_next(self, next_cond: Condition, operator: str) -> Condition:
        """Append the given condition to the chain

        Args:
            next_cond: Condition
            operator: Logical operator

        Returns: Condition
        """

        next_cond.operator_logical = operator
        self.selection.append(next_cond)
        return self

    def __and__(self, next_cond: Condition) -> Condition:
        """Appends ^ Condition to chain"""

        return self._set_next(next_cond, LogicalOperator.AND)

    def __or__(self, next_cond: Condition) -> Condition:
        """Appends ^OR Condition to chain"""

        return self._set_next(next_cond, LogicalOperator.OR)

    def __xor__(self, next_cond: Condition) -> Condition:
        """Appends ^NQ Condition to chain"""

        return self._set_next(next_cond, LogicalOperator.NQ)
