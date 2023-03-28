from pysdql.query.tpch.const import (LINEITEM_TYPE)

from pysdql.extlib.sdqlpy.sdql_lib import *

@sdql_compile({"li": LINEITEM_TYPE})
def query(li):

    # Insert
    df_aggr_1_0 = df_aggr_1.sum(lambda x: {x[0].concat(record({"l_extendedpricel_discount": ((x[0].l_extendedprice) * (x[0].l_discount))})): x[1]})
    
    df_aggr_1_1 = df_aggr_1_0.sum(lambda x: {record({"l_extendedpricel_discount": x[0].l_extendedpricel_discount}): True})
    
    df_aggr_1_2 = df_aggr_1_1.sum(lambda x: record({"l_extendedpricel_discount": x[0].l_extendedpricel_discount}))
    
    results = {df_aggr_1_2: True}
    # Complete

    return results
