from .operators import LogicalOperator


class Condition:
    def __init__(self, key, operator, value=None):
        self.operand_left = key
        self.operand_right = value
        self.operator_conditional = operator
        self.operator_logical = None
        self.selection = [self]

    @property
    def __str__(self):
        return (
            (self.operator_logical or "") +
            self.operand_left +
            self.operator_conditional +
            self.operand_right
        )

    def _set_next(self, next_cond, operator):
        next_cond.operator_logical = operator
        self.selection.append(next_cond)
        return self

    def __and__(self, next_cond):
        return self._set_next(next_cond, LogicalOperator.AND)

    def __or__(self, next_cond):
        return self._set_next(next_cond, LogicalOperator.OR)

    def __xor__(self, next_cond):
        return self._set_next(next_cond, LogicalOperator.NQ)
