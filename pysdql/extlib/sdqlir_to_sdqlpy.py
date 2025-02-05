from pysdql.core.prototype.basic.sdql_ir import *
from pysdql.extlib.sdqlpy.sdql_lib import sr_dict

names = {
    "db->li_dataset": "li",
    "db->cu_dataset": "cu",
    "db->ord_dataset": "ord",
    "db->na_dataset": "na",
    "db->re_dataset": "re",
    "db->pa_dataset": "pa",
    "db->ps_dataset": "ps",
    "db->su_dataset": "su"
}

def GenerateSDQLPYCode(AST: Expr, cache):
    code = ""

    inputType = type(AST)

    if inputType == ConstantExpr:
        if type(AST.value) == str:
            code += str("\"" + AST.value + "\"")
        else:
            code += str(AST.value)
        return code
    elif inputType == RecAccessExpr:
        code += GenerateSDQLPYCode(AST.recExpr, cache)
        code += "."
        code += AST.name
        return code
    elif inputType == IfExpr:
        code += "("
        code += GenerateSDQLPYCode(AST.thenBodyExpr, cache)
        code += ") if ("
        code += GenerateSDQLPYCode(AST.condExpr, cache)
        code += ") else ("
        code += GenerateSDQLPYCode(AST.elseBodyExpr, cache)
        code += ")"
        return code
    elif inputType == AddExpr:
        code += "(("
        code += GenerateSDQLPYCode(AST.op1Expr, cache)
        code += ") + ("
        code += GenerateSDQLPYCode(AST.op2Expr, cache)
        code += "))"
        return code
    elif inputType == SubExpr:
        code += "(("
        code += GenerateSDQLPYCode(AST.op1Expr, cache)
        code += ") - ("
        code += GenerateSDQLPYCode(AST.op2Expr, cache)
        code += "))"
        return code
    elif inputType == MulExpr:
        code += "(("
        code += GenerateSDQLPYCode(AST.op1Expr, cache)
        code += ") * ("
        code += GenerateSDQLPYCode(AST.op2Expr, cache)
        code += "))"
        return code
    elif inputType == DivExpr:
        code += "(("
        code += GenerateSDQLPYCode(AST.op1Expr, cache)
        code += ") / ("
        code += GenerateSDQLPYCode(AST.op2Expr, cache)
        code += "))"
        return code
    elif inputType == DicLookupExpr:
        code += GenerateSDQLPYCode(AST.dicExpr, cache)
        code += "["
        code += GenerateSDQLPYCode(AST.keyExpr, cache)
        code += "]"
        return code
    elif inputType == LetExpr:
        code += GenerateSDQLPYCode(AST.varExpr, cache)
        code += " = "
        code += GenerateSDQLPYCode(AST.valExpr, cache)
        code += "\n"
        code += GenerateSDQLPYCode(AST.bodyExpr, cache)
        code += "\n"
        return code
    elif inputType == VarExpr:
        if AST.name in names.keys():
            code += names[AST.name]
        else:
            code += AST.name
        return code
    elif inputType == PairAccessExpr:
        code += GenerateSDQLPYCode(AST.pairExpr, cache)
        code += "["
        code += str(AST.index)
        code += "]"
        return code
    elif inputType == PromoteExpr:
        return code
    elif inputType == CompareExpr:
        code += GenerateSDQLPYCode(AST.leftExpr, cache)
        if AST.compareType == CompareSymbol.EQ:
            code += " == "
        elif AST.compareType == CompareSymbol.GT:
            code += " > "
        elif AST.compareType == CompareSymbol.GTE:
            code += " >= "
        elif AST.compareType == CompareSymbol.LT:
            code += " < "
        elif AST.compareType == CompareSymbol.LTE:
            code += " <= "
        elif AST.compareType == CompareSymbol.NE:
            code += " != "
        code += GenerateSDQLPYCode(AST.rightExpr, cache)
        return code
    elif inputType == SumExpr:
        code += GenerateSDQLPYCode(AST.dictExpr, cache)
        code += ".sum(lambda "
        code += GenerateSDQLPYCode(AST.varExpr, cache)
        code += ": "
        code += GenerateSDQLPYCode(AST.bodyExpr, cache)
        code += ")\n"
        return code
    elif inputType == DicConsExpr:
        code += "{"
        if (type(AST.initialPairs[0][0])==str):
            code += "\""
            code += AST.initialPairs[0][0]
            code += "\""
        else:
            code += GenerateSDQLPYCode(AST.initialPairs[0][0], cache)
        code += ": "
        code += GenerateSDQLPYCode(AST.initialPairs[0][1], cache)
        code += "}"
        # code += "sr_dict({"
        # if (type(AST.initialPairs[0][0])==str):
        #     code += "\""
        #     code += AST.initialPairs[0][0]
        #     code += "\""
        # else:
        #     code += GenerateSDQLPYCode(AST.initialPairs[0][0], cache)
        # code += ": "
        # code += GenerateSDQLPYCode(AST.initialPairs[0][1], cache)
        # code += "})"
        return code
    elif inputType == EmptyDicConsExpr:
        code += "{}"
        return code
    elif inputType == RecConsExpr:
        code += "record({"
        for k, v in AST.initialPairs:
            code += "\""
            code += k
            code += "\": "
            code += GenerateSDQLPYCode(v, cache)
            code += ", "
        code = code[:-2]
        code += "})"
        return code
    elif inputType == VecConsExpr:
        code += "vector({"
        for k in AST.exprList:
            code += GenerateSDQLPYCode(k, cache)
            code += ", "
        code = code[:-2]
        code += "})"
        return code
    elif inputType == ConcatExpr:
        code += GenerateSDQLPYCode(AST.rec1, cache)
        code += ".concat("
        code += GenerateSDQLPYCode(AST.rec2, cache)
        code += ")"
        return code
    elif inputType == ExtFuncExpr:
        if AST.symbol == ExtFuncSymbol.StartsWith:
            code += "startsWith("
            code += GenerateSDQLPYCode(AST.inp1, cache)
            code += ", "
            code += GenerateSDQLPYCode(AST.inp2, cache)
            code += ")"
        elif AST.symbol == ExtFuncSymbol.EndsWith:
            code += "endsWith("
            code += GenerateSDQLPYCode(AST.inp1, cache)
            code += ", "
            code += GenerateSDQLPYCode(AST.inp2, cache)
            code += ")"
        elif AST.symbol == ExtFuncSymbol.FirstIndex:
            code += "firstIndex("
            code += GenerateSDQLPYCode(AST.inp1, cache)
            code += ", "
            code += GenerateSDQLPYCode(AST.inp2, cache)
            code += ")"
        elif AST.symbol == ExtFuncSymbol.ExtractYear:
            code += "extractYear("
            code += GenerateSDQLPYCode(AST.inp1, cache)
            code += ")"
        elif AST.symbol == ExtFuncSymbol.SubStr:
            code += "substr("
            print(AST.inp1)
            code += GenerateSDQLPYCode(AST.inp1, cache)
            code += ", "
            code += GenerateSDQLPYCode(AST.inp2, cache)
            code += ", "
            code += GenerateSDQLPYCode(AST.inp3, cache)
            code += ")"
        elif AST.symbol == ExtFuncSymbol.DictSize:
            code += "dictSize("
            code += GenerateSDQLPYCode(AST.inp1, cache)
            code += ")"
        else:
            print("Error: ExtFunc not defined!")
        return code
    elif inputType == sr_dict:
        code += "sr_dict({"
        for k in AST.getContainer().keys():
            code += ""
            code += GenerateSDQLPYCode(k, cache)
            code += ": "
            code += GenerateSDQLPYCode(AST.getContainer()[k], cache)
            code += ", "
        code = code[:-2]
        code += "})"
        return code
    else:
        print("Error: Unknown AST: " + str(type(AST)))
        print(AST)
        return