from pysdql.query.tpch.const import (PARTSUPP_TYPE, PART_TYPE, SUPPLIER_TYPE)

from pysdql.extlib.sdqlpy.sdql_lib import *


@sdql_compile({"ps": PARTSUPP_TYPE, "pa": PART_TYPE, "su": SUPPLIER_TYPE})
def query(ps, pa, su):
    # Insert
    brand45 = "Brand#45"
    mediumpolished = "MEDIUM POLISHED"
    customer = "Customer"
    complaints = "Complaints"
    part_0 = pa.sum(lambda x: ({x[0]: x[1]}) if (((((x[0].p_brand != brand45) * (startsWith(x[0].p_type, mediumpolished) == False))) * (((((((((((((((x[0].p_size == 9) + (x[0].p_size == 36))) + (x[0].p_size == 49))) + (x[0].p_size == 14))) + (x[0].p_size == 23))) + (x[0].p_size == 45))) + (x[0].p_size == 19))) + (x[0].p_size == 3))))) else (None))
    
    part_partsupp_index = part_0.sum(lambda x: {record({"p_partkey": x[0].p_partkey, "p_brand": x[0].p_brand, "p_type": x[0].p_type, "p_size": x[0].p_size}): True})
    
    supplier_0 = su.sum(lambda x: ({x[0]: x[1]}) if (((firstIndex(x[0].s_comment, customer) != ((-1) * (1))) * (firstIndex(x[0].s_comment, complaints) > ((firstIndex(x[0].s_comment, customer)) + (7))))) else (None))
    
    supplier_1 = supplier_0.sum(lambda x: {record({"s_suppkey": x[0].s_suppkey}): True})
    
    supplier_partsupp_isin_build_index = supplier_1.sum(lambda x: {x[0].s_suppkey: True})
    
    part_partsupp_probe = ps.sum(lambda x: ({x[0]: x[1]}) if (supplier_partsupp_isin_build_index[x[0].ps_suppkey] == None) else (None))
    
    part_partsupp_build_nest_dict = part_partsupp_index.sum(lambda x: {x[0].p_partkey: sr_dict({x[0]: x[1]})})
    
    part_partsupp_0 = part_partsupp_probe.sum(lambda x: (part_partsupp_build_nest_dict[x[0].ps_partkey].sum(lambda y: {x[0].concat(y[0]): True})
    ) if (part_partsupp_build_nest_dict[x[0].ps_partkey] != None) else (None))
    
    part_partsupp_1 = part_partsupp_0.sum(lambda x: {record({"p_brand": x[0].p_brand, "p_type": x[0].p_type, "p_size": x[0].p_size}): record({"supplier_cnt": 1.0})})
    
    results = part_partsupp_1.sum(lambda x: {x[0].concat(x[1]): True})
    
    # Complete

    return results
