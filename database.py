import sqlite3
import pandas as pd



# create connection by using object
# to connect with hotel_data database
connection = sqlite3.connect('test_user_data.db')
connection = connection.cursor()


'''
# importing required libraries
import mysql.connector

connection = mysql.connector.connect(
host ="db4free.net",
database="testdb25",
port=3306,
user ="testdb25",
passwd ="lobhik123"
)

# preparing a cursor object
connection = connection.cursor()

# creating database
connection.execute("CREATE DATABASE geeks4geeks")


'''


# connection.execute(table)
file = pd.read_excel("Chandrapur.xlsx",sheet_name="74_75 sheet")
#print(file)


#exit()
for index, row in file.iterrows():
    #if index > 3:
        print(index, row['SR NO'],row['Voter Name'],row['Voter Name En'],row['ID CARD NO'],row['GENDER'],row['AGE'],row['FAMILY'],row['AC NO'],row['PART NO'])
    #print(row['SR NO'],row['Name'])

        #exit()
  
        
        connection.execute('''INSERT INTO user_details(sr_no,full_name,full_name_en,id_card_no,gender,age,family,ac_no,part_no) 
                        VALUES ({},"{}","{}",'{}','{}',{},{},{},{})'''.format(row['SR NO'],row['Voter Name'],row['Voter Name En'],row['ID CARD NO'],row['GENDER'],row['AGE'],row['FAMILY'],row['AC NO'],row['PART NO']))
        
        #print(connection)

        connection.connection.commit()


exit()


# connection.execute( '''
#                    INSERT INTO GEEK (Email, First_Name,Last_Name, Score) VALUES ('{}','{}','{}',{} )
#                    '''.format("ALTER","ggggg","lobhik",87))

#connection.execute("INSERT INTO GEEK VALUES (3,'werre@gmail.com','test_name','test_lastname',3 )")

connection.connection.commit()


# df = pd.read_csv('csvdata.csv')

# df.to_sql()






# # insert query to insert food  details in
# # the above table
# connection.execute("INSERT INTO hotel VALUES (1, 'cakes',800,10 )")
# connection.execute("INSERT INTO hotel VALUES (2, 'biscuits',100,20 )")
# connection.execute("INSERT INTO hotel VALUES (3, 'chocos',1000,30 )")
 
 

#  # Creating table
# table = """ CREATE TABLE GEEK (
#             id int PRIMARY KEY   NOT NULL,
#             Email VARCHAR(255) NOT NULL,
#             First_Name CHAR(25) NOT NULL,
#             Last_Name CHAR(25),
#             Score INT
#         ); """
 
# connection.execute(table)



#  # Creating table
# table = """ CREATE TABLE test_user_details (
#             id int PRIMARY KEY   NOT NULL,
#             sr_no int NOT NULL,
#             full_name_mr VARCHAR(400) ,
#             full_name VARCHAR(400),
#             id_no VARCHAR(50),
#             gender VARCHAR(50),
#             age int,
#             family int
#         ); """
 
   #   connection.execute('''INSERT INTO MH_Districts(sr_no,district) 
   #                     VALUES ('{}','{}')'''.format(row['Sr_No'],row['Districts']))