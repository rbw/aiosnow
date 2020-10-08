from __future__ import annotations

from typing import Union

from .operators import LogicalOperator


class Condition:
    def __init__(self, key: str, operator: str, value: Union[str, int, None]):
        self.operand_left = key
        self.operand_right = value
        self.operator_conditional = operator
        self.operator_logical = ""
        self.registry = [self]

    def __str__(self) -> str:
        return self.serialize()

    def serialize(self, cond: Condition = None) -> str:
        c = cond or self
        return "".join(
            [
                c.operator_logical,
                c.operand_left,
                c.operator_conditional,
                str(c.operand_right),
            ]
        )

    def serialize_registry(self) -> str:
        """Condition string representation

        Returns: sysparm query
        """

        chain = ""

        for c in self.registry:
            chain += self.serialize(c)

        return chain

    def _merge_registry(self, registry: list) -> None:
        self.registry += registry

    def _add_condition(self, cond: Condition, operator: str) -> Condition:
        """Adds a new condition to chain

        Args:
            cond: Condition
            operator: Logical operator

        Returns: self
        """

        cond.operator_logical = str(operator)
        self._merge_registry(cond.registry)

        return self

    def __and__(self, next_cond: Condition) -> Condition:
        """Appends ^ Condition to chain"""

        return self._add_condition(next_cond, LogicalOperator.AND)

    def __or__(self, next_cond: Condition) -> Condition:
        """Appends ^OR Condition to chain"""

        return self._add_condition(next_cond, LogicalOperator.OR)

    def __xor__(self, next_cond: Condition) -> Condition:
        """Appends ^NQ Condition to chain"""

        return self._add_condition(next_cond, LogicalOperator.NQ)
