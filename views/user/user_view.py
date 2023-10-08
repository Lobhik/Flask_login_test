
import json

from flask import jsonify
from comman_use.comman import mandatoryCheck
from models.models import BaseModel
import pandas as pd

##
def UserDetailsController(table_name, post_data):

  list1=["name_en"]
  flag=mandatoryCheck(list1,post_data)
  if(flag==0):
    return {"data":False, "respMessage":"Please enter all mandatory fields !", "pageNum":0}
  where_clause = "name_en LIKE '{}%'".format(post_data['name_en'])

  bm = BaseModel(table_name)
  if 'assembly_no' in post_data and 'name_en' in post_data:
    where_clause = "ac_no = '{}' AND name_en LIKE '{}%' ".format(post_data['assembly_no'],post_data['name_en'])
  
  if 'assembly_no' in post_data and 'name_en' in post_data and 'village_no' in post_data:
    where_clause = "ac_no = '{}' and part_no = '{}' AND name_en LIKE '{}%' ".format(post_data['assembly_no'],post_data['village_no'],post_data['name_en'])

  select_columns = ["id","sr_no","name","ac_no","part_no","age","family","gender","name_en",
    "(SELECT village FROM all_district_list WHERE assembly_no = user_details.ac_no AND village_no = user_details.part_no) AS village_name",
    "(SELECT district FROM all_district_list WHERE assembly_no = user_details.ac_no AND village_no = user_details.part_no) AS district "
    ]

  #order_by = "id DESC"

  
  rows = bm.selectAll(select_column=",".join(select_columns), where_clause=where_clause, limit=0)
  if type(rows) is not str:
    #rowCount = bm.countAll(where_clause=where_clause)
    return jsonify(rows)
  else:
    return {"data":False, "msg":"Unble to process the data"}


