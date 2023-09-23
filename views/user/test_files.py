import pandas as pd
from models.models import BaseModel
import json

def TestInsertController(table_name):
    bm = BaseModel(table_name)
 
    file = pd.read_excel("ALL_DIST.xlsx")
    print(file)


    #exit()  
    for index, row in file.iterrows():
        if row["DIST"] == "Chandrapur":
            #print(index, row['NO'],row['DIST'],row['PART NO'])
            bi = bm.saveData({
                    "list_number":row['NO'],
                    "dist":row['DIST'],
                    "ass_no":row['ASS NO'],
                    "as_name":row['ASS'],
                    "part_no":row['PART NO'],
                    "part_name":row['PART']
                    })
            if type(bi) is not int:
                return {"respMessage":"unble to insert", "pageNum":0}
                    #  connection.execute('''INSERT INTO all_dist(list_number,dist,ass_no,as_name,part_no,part_name) 
                    #         VALUES ({},'{}',{},'{}','{}',"{}")'''.format(row['NO'],row['DIST'],row['ASS NO'],row['ASS'],row['PART NO'],row['PART']))
            


def TestInsertController(table_name):
    bm = BaseModel(table_name)
 
    file = pd.read_excel("ALL_DIST.xlsx")
    print(file)


    #exit()  
    for index, row in file.iterrows():
        if row["DIST"] == "Chandrapur":
            #print(index, row['NO'],row['DIST'],row['PART NO'])
            bi = bm.saveData({
                    "list_number":row['NO'],
                    "dist":row['DIST'],
                    "ass_no":row['ASS NO'],
                    "as_name":row['ASS'],
                    "part_no":row['PART NO'],
                    "part_name":row['PART']
                    })
            if type(bi) is not int:
                return {"respMessage":"unble to insert", "pageNum":0}
                    #  connection.execute('''INSERT INTO all_dist(list_number,dist,ass_no,as_name,part_no,part_name) 
                    #         VALUES ({},'{}',{},'{}','{}',"{}")'''.format(row['NO'],row['DIST'],row['ASS NO'],row['ASS'],row['PART NO'],row['PART']))
            




#   data = True

#   if post_data is not None:
#     bm.beginTransaction()
#     try:
#       bi = bm.saveData(post_data)
#       msg = EN.VESSEL_FILE_DATA_SAVE

#       if type(bi) is not int:
#         msg = bi
#         data = False
#       bm.closeTransaction()
#       return sendResponse(data, respMessage=msg, pageNum=0)
#     except Exception as e:
#       sendResponse(False, respMessage=e.__class__.__str__(e), pageNum=0)
#   else:
#     return sendResponse(False, respMessage=bi, pageNum=0)
