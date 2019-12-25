from marshmallow import fields

from .operators import LogicalOperator


class QueryBuilder:
    def __init__(self, root):
        self.tokens = root.tokens

    @property
    def sysparms(self):
        query = ""
        print(self.tokens)

        for token in self.tokens:
            print(token.__dict__)

        """if isinstance(token, LogicalOperator):
            query += token.value
        elif isinstance(token, tuple):
            for k in token:
                if isinstance(k, StringOperator):
                    query += k.value
                else:
                    query += k"""

        return query


class Condition:
    op_conditional = None
    op_logical = None
    value = None

    def __init__(self, key, condition, value=None):
        self.key = key
        self.condition = condition
        self.value = value

    @property
    def __dict__(self):
        return dict(
            logical=self.op_logical,
            conditional=self.op_conditional,
            key=self.key,
            value=self.value
        )

    tokens = []

    def _push_condition(self):
        self.tokens.append(self)

    def __and__(self, cond):
        self.op_logical = LogicalOperator.AND
        return cond

    def __or__(self, cond):
        self.op_logical = LogicalOperator.OR
        return cond

    def __xor__(self, cond):
        self.op_logical = LogicalOperator.NQ
        return cond

    def eq(self, value):
        raise NotImplementedError
