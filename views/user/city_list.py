
from flask import jsonify

from models.models import BaseModel


def CityListController(table_name, ct, ac, pt,limit,page):
  bm = BaseModel(table_name)
  where_clause = "id <> 0 GROUP BY district"
  #test_user_details
  if ct is not None and ct != 0:
    where_clause = "`district` Like '{}' GROUP BY assembly_no ".format(ct)
    if ac > 0:
      where_clause = " `district` Like '{}' AND `assembly_no` = {} GROUP BY village_no".format(ct,ac)
      if pt > 0:
        where_clause = "`district` Like '{}' AND `assembly_no` = {} AND `village_no` = {}".format(ct,ac,pt)

  
  select_columns = ["id","district","assembly_no ","assembly","village_no","village"]
  order_by = "id ASC"

  
  rows = bm.selectAll(select_column= ",".join(select_columns),where_clause= where_clause, limit=limit, page=page, order_by=order_by)
  if type(rows) is not str:
    #rowCount = bm.countAll(where_clause=where_clause)
    return {"data":rows}
  else:
    return {False}