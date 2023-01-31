from pysdql.core.dtypes.SDQLIR import SDQLIR
from pysdql.core.dtypes.CondExpr import CondExpr
from pysdql.core.dtypes.ColExpr import ColExpr
from pysdql.core.dtypes.EnumUtil import MathSymbol, LogicSymbol

from pysdql.core.dtypes.sdql_ir import *


class ExternalExpr(SDQLIR):
    def __init__(self, col, ext_func, args=None, isinvert=False):
        self.col = col
        self.func = ext_func
        self.args = args

        self.vars = {}

        self.isinvert = isinvert

    def replace(self, rec, inplace=False, mapper=None):
        return ExternalExpr(self.col.replace(rec, inplace, mapper), self.func, self.args, self.isinvert)

    def gen_cond_expr(self, operator, unit2):
        """
        :param operator: CompareSymbol
        :param unit2: ColEl | (float, int, str) | date@str
        :return:
        """
        if operator == CompareSymbol.EQ:
            if type(unit2) == str:
                self.col.add_const(unit2)
                return CondExpr(unit1=self, operator=operator, unit2=self.col.get_const_var(unit2))
            return CondExpr(unit1=self,
                            operator=operator,
                            unit2=unit2)

        return CondExpr(unit1=self,
                        operator=operator,
                        unit2=unit2)

    def __eq__(self, other) -> CondExpr:
        """
        Equal
        :param other:
        :return:
        """
        return self.gen_cond_expr(operator=CompareSymbol.EQ,
                                  unit2=other)
        # if type(other) == str:
        #     self.add_const(other)
        #     return CondExpr(unit1=self.col, operator=CompareSymbol.EQ, unit2=self.get_const_var(other))
        # return CondExpr(unit1=self.col, operator=CompareSymbol.EQ, unit2=input_fmt(other))

    def __ne__(self, other) -> CondExpr:
        """
        Not equal
        :param other:
        :return:
        """
        return self.gen_cond_expr(operator=CompareSymbol.NE,
                                  unit2=other)
        # return CondExpr(unit1=self.col, operator=CompareSymbol.NE, unit2=input_fmt(other))

    def __lt__(self, other) -> CondExpr:
        """
        Less than
        :param other:
        :return:
        """
        return self.gen_cond_expr(operator=CompareSymbol.LT,
                                  unit2=other)
        # return CondExpr(unit1=self.col, operator=CompareSymbol.LT, unit2=input_fmt(other))

    def __le__(self, other) -> CondExpr:
        """
        Less than or Equal
        :param other:
        :return:
        """
        return self.gen_cond_expr(operator=CompareSymbol.LTE,
                                  unit2=other)
        # return CondExpr(unit1=self.col, operator=CompareSymbol.LTE, unit2=input_fmt(other))

    def __gt__(self, other) -> CondExpr:
        """
        Greater than
        :param other:
        :return:
        """
        return self.gen_cond_expr(operator=CompareSymbol.GT,
                                  unit2=other)
        # return CondExpr(unit1=self.col, operator=CompareSymbol.GT, unit2=input_fmt(other))

    def __ge__(self, other) -> CondExpr:
        """
        Greater than or Equal
        :param other:
        :return:
        """
        return self.gen_cond_expr(operator=CompareSymbol.GTE,
                                  unit2=other)
        # return CondExpr(unit1=self.col, operator=CompareSymbol.GTE, unit2=input_fmt(other))

    def __and__(self, other):
        return CondExpr(unit1=self,
                        operator=LogicSymbol.AND,
                        unit2=other)

    def __add__(self, other):
        return ColExpr(unit1=self,
                       operator=MathSymbol.ADD,
                       unit2=other)

    @property
    def sdql_ir(self):
        if isinstance(self.col, SDQLIR):
            col_expr = self.col.sdql_ir
        elif isinstance(self.col, Expr):
            col_expr = self.col
        else:
            raise TypeError(f'Illegal Column IR {type(self.col)} {self.col}')

        if self.func == ExtFuncSymbol.StartsWith:
            return ExtFuncExpr(self.func,
                               col_expr,
                               self.args,
                               ConstantExpr("Nothing!"))
        if self.func == ExtFuncSymbol.StringContains:
            return CompareExpr(CompareSymbol.NE,
                               ExtFuncExpr(ExtFuncSymbol.FirstIndex,
                                           col_expr,
                                           self.args,
                                           ConstantExpr("Nothing!")),
                               MulExpr(ConstantExpr(-1), ConstantExpr(1)))
        if self.func == ExtFuncSymbol.FirstIndex:
            return ExtFuncExpr(self.func,
                                col_expr,
                                self.args,
                                ConstantExpr("Nothing!"))

        if self.func == ExtFuncSymbol.ExtractYear:
            return ExtFuncExpr(self.func,
                                col_expr,
                                ConstantExpr("Nothing!"),
                                ConstantExpr("Nothing!"))

        raise NotImplementedError(f'''
        {self.col},
        {self.func}
        ''')

    def __repr__(self):
        return str(self.sdql_ir)
