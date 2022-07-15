class CondUnit:
    def __init__(self, unit1, operator: str, unit2, inherit_from=None):
        self.unit1 = unit1
        self.op = operator
        self.unit2 = unit2
        self.inherit_from = inherit_from

    def inherit(self, other):
        if type(other) == CondUnit:
            if other.inherit_from:
                if self.inherit_from:
                    self.inherit_from.inherit(other.inherit_from)
                else:
                    self.inherit_from = other.inherit_from
        return self

    def new_cond(self, new_str):
        from pysdql.core.dtypes.ColumnUnit import ColUnit
        if type(self.unit1) == ColUnit or type(self.unit1) == CondUnit:
            u1_str = self.unit1.new_expr(new_str)
        else:
            u1_str = str(self.unit1)
        if type(self.unit2) == ColUnit or type(self.unit2) == CondUnit:
            u2_str = self.unit2.new_expr(new_str)
        else:
            u2_str = str(self.unit2)

        return self.concat(u1_str, u2_str)

    def new_expr(self, new_str) -> str:
        from pysdql.core.dtypes.ColumnUnit import ColUnit
        if type(self.unit1) == ColUnit or type(self.unit1) == CondUnit:
            u1_str = self.unit1.new_expr(new_str)
        else:
            u1_str = str(self.unit1)
        if type(self.unit2) == ColUnit or type(self.unit2) == CondUnit:
            u2_str = self.unit2.new_expr(new_str)
        else:
            u2_str = str(self.unit2)

        if self.op in ['==', '<=', '<']:
            return f'({u1_str} {self.op} {u2_str})'
        if self.op == '>':
            return f'({u2_str} < {u1_str})'
        if self.op == '>=':
            return f'({u2_str} <= {u1_str})'
        if self.op == '!=':
            return f'not ({u1_str} == {u2_str})'
        if self.op == '&&':
            return f'({u1_str} {self.op} {u2_str})'
        if self.op == '||':
            return f'({u1_str}) {self.op} ({u2_str})'
        if self.op == '~':
            return f'not ({u1_str})'
        return f'({u1_str} {self.op} {u2_str})'

    def get_1st(self):
        return str(self.unit1)

    def get_2nd(self):
        return str(self.unit2)

    def concat(self, u1, u2):
        if self.op in ['<', '<=', '==', '!=', '&&', '||', '~']:
            return CondUnit(u1, self.op, u2).inherit(self)
        if self.op == '>':
            return CondUnit(u2, '<', u1).inherit(self)
        if self.op == '>=':
            return CondUnit(u2, '<=', u1).inherit(self)
        return CondUnit(u1, self.op, u2).inherit(self)

    @property
    def expr(self):
        if self.op in ['==', '<=', '<']:
            return f'({self.unit1} {self.op} {self.unit2})'
        if self.op == '>':
            return f'({self.unit2} < {self.unit1})'
        if self.op == '>=':
            return f'({self.unit2} <= {self.unit1})'
        if self.op == '!=':
            return f'not ({self.unit1} == {self.unit2})'
        if self.op == '&&':
            return f'({self.unit1} {self.op} {self.unit2})'
        if self.op == '||':
            return f'({self.unit1}) {self.op} ({self.unit2})'
        if self.op == '~':
            return f'not ({self.unit1})'
        return f'({self.unit1} {self.op} {self.unit2})'

    def __repr__(self):
        return self.expr

    def __and__(self, other):
        return CondUnit(unit1=self,
                        operator='&&',
                        unit2=other).inherit(other)

    def __rand__(self, other):
        return CondUnit(unit1=other,
                        operator='&&',
                        unit2=self).inherit(other)

    def __iand__(self, other):
        return CondUnit(unit1=other,
                        operator='&&',
                        unit2=self).inherit(other)

    def __or__(self, other):
        return CondUnit(unit1=self,
                        operator='||',
                        unit2=other).inherit(other)

    def __ror__(self, other):
        return CondUnit(unit1=other,
                        operator='||',
                        unit2=self).inherit(other)

    def __ior__(self, other):
        return CondUnit(unit1=self,
                        operator='||',
                        unit2=other).inherit(other)

    def __invert__(self):
        return CondUnit(unit1=self,
                        operator='~',
                        unit2=self).inherit(self)
