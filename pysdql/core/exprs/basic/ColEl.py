import re

from pysdql.core.exprs.advanced.ColOpExprs import (
    ColOpExternal,
    ColOpBinary,
    ColOpIsNull,
)
from pysdql.core.exprs.advanced.ColOpIsinExpr import ColOpIsin
from pysdql.core.exprs.complex.AggrExpr import AggrExpr
from pysdql.core.exprs.advanced.BinCondExpr import BinCondExpr
from pysdql.core.enums.EnumUtil import (
    MathSymbol,
    AggrType,
    OpRetType,
)
from pysdql.core.interfaces.availability.Replaceable import Replaceable
from pysdql.core.exprs.advanced.FreeStateExprs import FreeStateVar
from pysdql.core.exprs.carrier.OpExpr import OpExpr
from pysdql.core.prototype.basic.sdql_ir import (
    CompareSymbol,
    ExtFuncSymbol,
    RecAccessExpr,
    ConstantExpr,
)


class ColEl(Replaceable):
    def __init__(self, col_of, col_name: str, promoted=None):
        """
        :param col_of: DataFrame
        :param col_name:
        """
        self.__relation = col_of
        self.__field = col_name
        self.promoted = promoted
        self.follow_promotion = None
        self.data_type = ''

        self.isvar = False
        self.var_name = ''

    def add_const(self, const):
        self.relation.add_const(const)

    def get_const_var(self, const):
        return self.relation.get_const_var(const)

    @property
    def relation(self):
        return self.__relation

    @property
    def R(self):
        return self.__relation

    @property
    def field(self):
        return self.__field

    @property
    def col_of(self):
        return self.__relation

    @property
    def col_name(self):
        return self.__field

    @property
    def col(self):
        return self.relation.key_access(self.field)

    @property
    def year(self):
        return ColOpExternal(col=self, ext_func=ExtFuncSymbol.ExtractYear)

    @property
    def month(self):
        raise NotImplementedError

    @property
    def day(self):
        raise NotImplementedError

    def new_expr(self, new_str) -> str:
        if self.isvar:
            if self.promoted:
                f'promote[real]({self.var_name})'
            return f'{self.var_name}'
        return f'{new_str}.{self.field}'

    @property
    def from_1DT(self):
        if self.relation.structure == '1DT':
            return True
        else:
            return False
        # from pysdql.core.dtypes.relation import relation
        # if type(self.relation) == relation:
        #     return True
        # else:
        #     return False

    @property
    def from_LRT(self):
        if self.relation.structure == 'LRT':
            return True
        else:
            return False
        # from pysdql.core.dtypes.JoinExpr import JoinExpr
        # if type(self.dataframe) == JoinExpr:
        #     return True
        # else:
        #     return False

    @property
    def from_GRP(self):
        if self.relation.structure == 'GRP':
            return True
        else:
            return False

    # @property
    # def key(self):
    #     if self.from_1DT:
    #         return self.relation.el.k
    #     if self.from_LRT:
    #         if self.field in self.relation.left.columns:
    #             return f'{self.relation.el.k}.left'
    #         if self.field in self.relation.right.columns:
    #             return f'{self.relation.el.k}.right'
    #     if self.from_GRP:
    #         if self.field in self.relation.groupby.columns:
    #             return self.relation.el.k
    #
    # @property
    # def val(self):
    #     if self.from_1DT:
    #         return self.relation.el.v
    #     if self.from_LRT:
    #         return self.relation.el.v
    #     if self.from_GRP:
    #         return 1

    @property
    def expr(self) -> str:
        return f'{self.relation.el.k}.{self.field}'
        # if self.isvar:
        #     if self.promoted:
        #         f'promote[real]({self.var_name})'
        #     return self.var_name
        # if self.from_LRtuple:
        #     if self.name in self.dataframe.left.cols:
        #         return f'{self.dataframe.el.k}.left.{self.name}'
        #     if self.name in self.dataframe.right.cols:
        #         return f'{self.dataframe.el.k}.right.{self.name}'
        #     else:
        #         raise ValueError()
        # if self.follow_promotion:
        #     return f'{self.follow_promotion}({self.dataframe.el.k}.{self.name})'
        # return f'{self.dataframe.el.k}.{self.name}'

    @property
    def sdql_expr(self) -> str:
        return f'{self.relation.el.k}.{self.field}'

    def __str__(self):
        return self.sdql_expr

    def __repr__(self):
        return self.expr

    def __hash__(self):
        return hash((self.R.el.k, self.R.el.v, self.R.name, self.field))

    '''
    Comparison Operations
    '''

    def gen_cond_expr(self, operator, unit2):
        """
        :param operator: ColEl
        :param unit2: ColEl | (float, int, str) | date@str
        :return:
        """
        if operator == CompareSymbol.EQ or operator == CompareSymbol.NE:
            if type(unit2) == str:
                self.add_const(unit2)
                return BinCondExpr(unit1=self, operator=operator, unit2=self.get_const_var(unit2))
            return BinCondExpr(unit1=self,
                               operator=operator,
                               unit2=unit2)

        return BinCondExpr(unit1=self,
                           operator=operator,
                           unit2=unit2)

    def __eq__(self, other) -> BinCondExpr:
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

    def __ne__(self, other) -> BinCondExpr:
        """
        Not equal
        :param other:
        :return:
        """
        return self.gen_cond_expr(operator=CompareSymbol.NE,
                                  unit2=other)
        # return CondExpr(unit1=self.col, operator=CompareSymbol.NE, unit2=input_fmt(other))

    def __lt__(self, other) -> BinCondExpr:
        """
        Less than
        :param other:
        :return:
        """
        return self.gen_cond_expr(operator=CompareSymbol.LT,
                                  unit2=other)
        # return CondExpr(unit1=self.col, operator=CompareSymbol.LT, unit2=input_fmt(other))

    def __le__(self, other) -> BinCondExpr:
        """
        Less than or Equal
        :param other:
        :return:
        """
        return self.gen_cond_expr(operator=CompareSymbol.LTE,
                                  unit2=other)
        # return CondExpr(unit1=self.col, operator=CompareSymbol.LTE, unit2=input_fmt(other))

    def __gt__(self, other) -> BinCondExpr:
        """
        Greater than
        :param other:
        :return:
        """
        return self.gen_cond_expr(operator=CompareSymbol.GT,
                                  unit2=other)
        # return CondExpr(unit1=self.col, operator=CompareSymbol.GT, unit2=input_fmt(other))

    def __ge__(self, other) -> BinCondExpr:
        """
        Greater than or Equal
        :param other:
        :return:
        """
        return self.gen_cond_expr(operator=CompareSymbol.GTE,
                                  unit2=other)
        # return CondExpr(unit1=self.col, operator=CompareSymbol.GTE, unit2=input_fmt(other))

    '''
    Arithmetic Operations
    '''

    def __add__(self, other):
        return ColOpBinary(unit1=self,
                           operator=MathSymbol.ADD,
                           unit2=other)
        # return ColExpr(value=AddExpr(self.col, input_fmt(other)), relation=self.R)

    def __mul__(self, other):
        return ColOpBinary(unit1=self,
                           operator=MathSymbol.MUL,
                           unit2=other)
        # return ColExpr(value=MulExpr(self.col, input_fmt(other)), relation=self.R)

    def __sub__(self, other):
        return ColOpBinary(unit1=self,
                           operator=MathSymbol.SUB,
                           unit2=other)
        # return ColExpr(value=SubExpr(self.col, input_fmt(other)), relation=self.R)

    def __truediv__(self, other):
        return ColOpBinary(unit1=self,
                           operator=MathSymbol.DIV,
                           unit2=other)
        # return ColExpr(value=DivExpr(self.col, input_fmt(other)), relation=self.R)

    '''
    Reverse Arithmetic Operations
    '''

    def __radd__(self, other):
        return ColOpBinary(unit1=other,
                           operator=MathSymbol.ADD,
                           unit2=self)
        # return ColExpr(value=AddExpr(input_fmt(other), self.col), relation=self.R)

    def __rmul__(self, other):
        return ColOpBinary(unit1=other,
                           operator=MathSymbol.MUL,
                           unit2=self)
        # return ColExpr(value=MulExpr(input_fmt(other), self.col), relation=self.R)

    def __rsub__(self, other):
        return ColOpBinary(unit1=other,
                           operator=MathSymbol.SUB,
                           unit2=self)
        # return ColExpr(value=SubExpr(input_fmt(other), self.col), relation=self.R)

    def __rtruediv__(self, other):
        return ColOpBinary(unit1=other,
                           operator=MathSymbol.DIV,
                           unit2=self)
        # return ColExpr(value=DivExpr(input_fmt(other), self.col), relation=self.R)

    def isin(self, vals):
        if type(vals) == list or type(vals) == tuple:
            if len(vals) == 0:
                raise ValueError()
            if len(vals) == 1:
                return vals[0]

            tmp_list = []
            for i in vals:
                tmp_list.append(self.gen_cond_expr(operator=CompareSymbol.EQ,
                                                   unit2=i))

            a = tmp_list.pop()
            b = tmp_list.pop()

            tmp_cond = a | b

            if tmp_list:
                for i in tmp_list:
                    tmp_cond |= i

            return tmp_cond

        if isinstance(vals, ColEl):
            part_on = vals.relation.create_copy()

            isin_expr = ColOpIsin(col_probe=self, col_part=part_on.get_col(vals.field))

            for k in part_on.context_constant:
                self.add_const(k)

            self.relation.push(OpExpr(op_obj=isin_expr,
                                      op_on=self.relation,
                                      op_iter=True,
                                      iter_on=None,
                                      ret_type=None))

            part_on.push(OpExpr(op_obj=isin_expr,
                                      op_on=self.relation,
                                      op_iter=True,
                                      iter_on=None,
                                      ret_type=None))

            return isin_expr

    @property
    def dt(self):
        self.data_type = 'date'
        return self

    @property
    def str(self):
        self.data_type = 'str'
        return self

    @property
    def date(self):
        self.data_type = 'date'
        return self

    @property
    def int(self):
        self.data_type = 'int'
        return self

    @property
    def real(self):
        self.data_type = 'real'
        return self

    def startswith(self, pattern: str):
        # A%
        self.add_const(pattern)
        return ColOpExternal(self, ExtFuncSymbol.StartsWith, self.get_const_var(pattern))
        # return ExternalExpr(self, 'StrStartsWith', pattern)

    def endswith(self, pattern: str):
        # %B
        self.add_const(pattern)
        return ColOpExternal(self, ExtFuncSymbol.EndsWith, self.get_const_var(pattern))

    def contains(self, pattern, regex=False):
        # %A%
        if regex:
            return self.match_regex(pattern)
        else:
            self.add_const(pattern)
            return ColOpExternal(self, ExtFuncSymbol.StringContains, self.get_const_var(pattern))

    def slice(self, start, end):
        # substring
        return ColOpExternal(self, ExtFuncSymbol.SubStr, (start, end))

    def find(self, pattern):
        self.add_const(pattern)
        return ColOpExternal(self, ExtFuncSymbol.FirstIndex, self.get_const_var(pattern))

    def promote(self, func):
        self.follow_promotion = f'promote[{func}]'
        return self

    def sum(self):
        aggr_expr = AggrExpr(aggr_type=AggrType.Scalar,
                             aggr_on=self.relation,
                             aggr_op={self.field: self.sdql_ir},
                             aggr_else=ConstantExpr(0.0),
                             origin_dict={self.field: (self.field, 'sum')},
                             is_single_col_op=True)

        op_expr = OpExpr(op_obj=aggr_expr,
                         op_on=self.relation,
                         op_iter=True,
                         iter_on=self.relation,
                         ret_type=OpRetType.FLOAT)

        self.relation.push(op_expr)

        return aggr_expr

    def count(self):
        raise NotImplementedError
        pass

    def mean(self):
        aggr_expr = AggrExpr(aggr_type=AggrType.Scalar,
                             aggr_on=self.relation,
                             aggr_op={self.field: self.sdql_ir},
                             aggr_else=ConstantExpr(0.0),
                             origin_dict={self.field: (self.field, 'mean')},
                             is_single_col_op=True)

        op_expr = OpExpr(op_obj=aggr_expr,
                         op_on=self.relation,
                         op_iter=True,
                         iter_on=self.relation,
                         ret_type=OpRetType.FLOAT)

        self.relation.push(op_expr)

        return aggr_expr

    def min(self):
        raise NotImplementedError
        pass

    def max(self):
        raise NotImplementedError
        pass

    def replace(self, rec, inplace=False, mapper=None):
        # print(self.field, rec, inplace, mapper)
        if mapper:
            if isinstance(mapper, dict):
                for k in mapper.keys():
                    if isinstance(k, (tuple, list)):
                        if self.field in k:
                            if inplace:
                                return mapper[k]
                            else:
                                return RecAccessExpr(mapper[k], self.field)
                    elif isinstance(k, str):
                        if self.field == k:
                            if inplace:
                                return mapper[k]
                            else:
                                return RecAccessExpr(mapper[k], self.field)
                else:
                    return self.sdql_ir
                    # raise ValueError(f'cannot find {self.field}')
            else:
                raise TypeError(f'mapper must be a dict')

        if inplace:
            return rec

        return RecAccessExpr(rec, self.field)

    '''
    FlexIR
    '''

    @property
    def replaceable(self):
        return True

    @property
    def oid(self):
        return hash((
            self.col_of.name,
            self.col_name
        ))

    @property
    def sdql_ir(self):
        return self.relation.key_access(self.field)

    def match_regex(self, pattern: str):
        num_of_substr = pattern.count('.*?')
        if num_of_substr == 0:
            raise NotImplementedError
        elif num_of_substr == 1:
            if pattern.endswith('.*?$'):
                # print(f'{pattern} is startswith')
                return self.startswith(pattern.replace('^', '').replace('.*?$', ''))
            if pattern.startswith('^.*?'):
                # print(f'{pattern} is endswith')
                return self.endswith(pattern.replace('^.*?', '').replace('$', ''))
        elif num_of_substr == 2:
            if pattern.startswith('^.*?') and pattern.endswith('.*?$'):
                # print(f'{pattern} is contains')
                return self.contains(pattern.replace('^.*?', '').replace('.*?$', ''))
        else:
            # print(f'{pattern} is contains in order')
            tmp_pattern = pattern.replace('^', '').replace('$', '')
            tmp_list = [i for i in re.split('\.\*\?', tmp_pattern) if i]
            tmp_cond = self.find(tmp_list[0]) != ConstantExpr(-1) * ConstantExpr(1)
            for i in range(len(tmp_list)):
                if i > 0:
                    tmp_cond &= self.find(tmp_list[i]) > (self.find(tmp_list[i - 1]) + (len(tmp_list[i - 1]) - 1))

            return tmp_cond
        # if re.match('^.*?[^\.\*\?].*?$', pattern):
        #     print(re.match('^.*?[^\.\*\?].*?$', pattern).group())

    def __getitem__(self, item):
        vname_suffix = f'{self.field}_el_{item}_'

        if item == 0:
            col_ins_list = self.relation.retriever.findall_col_insert_as_list()

            if self.field in col_ins_list.keys():
                target = col_ins_list[self.field][0]

                free_state_var = FreeStateVar(f'{vname_suffix}{target.descriptor}',
                                              target,
                                              self.relation)

                op_expr = OpExpr(op_obj=free_state_var,
                                 op_on=self.relation,
                                 op_iter=True,
                                 iter_on=self.relation,
                                 ret_type=OpRetType.FLOAT)

                self.relation.push(op_expr)

                return free_state_var
            else:
                raise IndexError(f'Invalid index {self.field} in {col_ins_list}')
        else:
            raise NotImplementedError

    def isnull(self):
        return ColOpIsNull(self)