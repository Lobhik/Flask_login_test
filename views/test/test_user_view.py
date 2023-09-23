import json
from models.models import BaseModel


def CityListController(table_name, ct, ac, pt,limit,page):
  bm = BaseModel(table_name)
  where_clause = "id <> 0 GROUP BY dist"
  #test_user_details
  if ct is not None:
    where_clause = "`dist` Like '{}' GROUP BY ass_no ".format(ct)
    if ac > 0:
      where_clause = " `dist` Like '{}' AND `ass_no` = {} GROUP BY part_no".format(ct,ac)
      if pt > 0:
        where_clause = "`dist` Like '{}' AND `ass_no` = {} AND `part_no` = {}".format(ct,ac,pt)

  
#   select_columns = ["id","ass_no","as_name","part_no","part_name","dist"

#     ]
  select_columns = ["JSON_OBJECT('id', id,'district',dist,'district_zone_no', ass_no,'district_zone', as_name,'village',part_name,'village_no',part_no)"
    ]

  order_by = "id ASC"

  
  rows = bm.selectAll(select_column= ",".join(select_columns),where_clause= where_clause, limit=limit, page=page, order_by=order_by)
  result = [json.loads(item[0]) for item in rows]

  #for i in rows:
  print(rows)
  if type(rows) is not str:
    rowCount = bm.countAll(where_clause=where_clause)
    return {"data":result}
  else:
    return {False}