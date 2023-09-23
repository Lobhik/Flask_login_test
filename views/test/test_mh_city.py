import json
from models.models import BaseModel


def MHCityListController(table_name,limit,page):
  bm = BaseModel(table_name)
  where_clause = None
  #test_user_details
  select_columns = ["JSON_OBJECT('id',id,'sr_no',sr_no,'district',district)"]
 
#   select_columns = ["id","ass_no","as_name","part_no","part_name","dist"

#     ]
    # select_columns = ["JSON_OBJECT('id', id,'district',dist,'district_zone', ass_no,'as_name', as_name,'village',part_name)"
    # ]

  order_by = "id DESC"

  
  rows = bm.selectAll(select_column= ",".join(select_columns),where_clause= where_clause, limit=limit, page=page, order_by=order_by)
  print("@@@",rows)
  result = [json.loads(item[0]) for item in rows]

  #for i in rows:
  print(rows)
  if type(rows) is not str:
    rowCount = bm.countAll(where_clause=where_clause)
    return {"data":result}
  else:
    return {False}