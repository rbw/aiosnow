from .operators import LogicalOperator


class Condition:
    instances = []

    def __init__(self, key, operator, value=None):
        self.operand_left = key
        self.operand_right = value
        self.operator_conditional = operator
        self.operator_logical = None
        self.instances.append(self)

    @property
    def __str__(self):
        return (
            self.operand_left +
            self.operator_conditional +
            self.operand_right +
            (self.operator_logical or "")
        )

    def __and__(self, cond):
        self.operator_logical = LogicalOperator.AND
        return cond

    def __or__(self, cond):
        self.operator_logical = LogicalOperator.OR
        return cond

    def __xor__(self, cond):
        self.operator_logical = LogicalOperator.NQ
        return cond
