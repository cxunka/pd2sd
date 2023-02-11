from pysdql.query.tpch.const import (LINEITEM_TYPE, CUSTOMER_TYPE, ORDERS_TYPE)

from pysdql.extlib.sdqlpy.sdql_lib import *


@sdql_compile({"li": LINEITEM_TYPE, "cu": CUSTOMER_TYPE, "ord": ORDERS_TYPE})
def query(li, cu, ord):

    # Insert
    v0 = li.sum(lambda x: (({record({"l_orderkey": x[0].l_orderkey}): record({"sum_quantity": x[0].l_quantity})}) if (True) else (None)) if (x[0] != None) else (None))
    
    v1 = v0.sum(lambda x: (({x[0].concat(x[1]): True}) if (True) else (None)) if (x[0] != None) else (None))
    
    v2 = v1.sum(lambda x: (({x[0]: x[1]}) if (x[0].sum_quantity > 300) else (None)) if (x[0] != None) else (None))
    
    v3 = v2.sum(lambda x: (({x[0]: x[1]}) if (True) else (None)) if (x[0] != None) else (None))
    
    isin_build = v3.sum(lambda x: (({x[0].l_orderkey: True}) if (True) else (None)) if (x[0] != None) else (None))
    
    v4 = ord.sum(lambda x: ((({x[0]: True}) if (isin_build[x[0].o_orderkey] != None) else (None)) if (True) else (None)) if (x[0] != None) else (None))
    
    customer_orders_lineitem_probe = v4
    isin_build = li.sum(lambda x: (({x[0].l_orderkey: True}) if (True) else (None)) if (x[0] != None) else (None))
    
    v0 = ord.sum(lambda x: ((({x[0]: True}) if (isin_build[x[0].o_orderkey] != None) else (None)) if (True) else (None)) if (x[0] != None) else (None))
    
    customer_orders_probe = v0
    v0 = cu.sum(lambda x: (({x[0]: x[1]}) if (True) else (None)) if (x[0] != None) else (None))
    
    customer_orders_part = v0
    build_side = customer_orders_part.sum(lambda x: (({x[0].c_custkey: sr_dict({x[0]: x[1]})}) if (True) else (None)) if (x[0] != None) else (None))
    
    v0 = customer_orders_probe.sum(lambda x: (({build_side[x[0].o_custkey].sum(lambda y: x[0].concat(y[0]))
    : True}) if (build_side[x[0].o_custkey] != None) else (None)) if (x[0] != None) else (None))
    
    v1 = v0.sum(lambda x: (({x[0]: x[1]}) if (True) else (None)) if (x[0] != None) else (None))
    
    customer_orders_lineitem_part = v1
    build_side = customer_orders_lineitem_part.sum(lambda x: (({x[0].o_orderkey: sr_dict({x[0]: x[1]})}) if (True) else (None)) if (x[0] != None) else (None))
    
    v0 = customer_orders_lineitem_probe.sum(lambda x: (({build_side[x[0].l_orderkey].sum(lambda y: x[0].concat(y[0]))
    : True}) if (build_side[x[0].l_orderkey] != None) else (None)) if (x[0] != None) else (None))
    
    v1 = v0.sum(lambda x: (({record({"c_name": x[0].c_name, "c_custkey": x[0].c_custkey, "o_orderkey": x[0].o_orderkey, "o_orderdate": x[0].o_orderdate, "o_totalprice": x[0].o_totalprice}): record({"sum_quantity": x[0].l_quantity})}) if (True) else (None)) if (x[0] != None) else (None))
    
    v2 = v1.sum(lambda x: (({x[0].concat(x[1]): True}) if (True) else (None)) if (x[0] != None) else (None))
    
    results = v2
    # Complete

    return results
