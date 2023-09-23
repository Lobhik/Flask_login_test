import os
#import mysql.connector
#from flaskext.mysql import MySQL
import pymysql
from flask import g
from pymysql.cursors import DictCursor
import sqlite3


"""
  DML command executor

  Base Model Class which is responsible to execute
  queries on Single Table.


"""


class BaseModel(object):
    """
  Class constructor

  @type table_name: str
  @param table_name: Table name on which we are going to execute DML commands
"""

    def __init__(self, table_name=None):
        self.begin_transaction = False
        self.table_name = table_name
        # self.connection = sqlite3.connect("test_user_data.db")
        # self.database_name = "test_user_data"

        self.connection = get_db_connection()
        self.database_name = g.db_name_lookup if 'db_host_lookup' in g and g.db_name_lookup is not None else "initial_db"
        #self.database_name = g.db_name_lookup if 'db_host_lookup' in g and g.db_name_lookup is not None else os.environ.get('DB_NAME')
        #self.database_name = g.db_name_lookup if 'db_host_lookup' in g and g.db_name_lookup is not None else "testdb25"
        
        self.clause_operator = {'eq': '=', 'gt': '>', 'lq': '<', 'gte': '>=', 'lqe': '<=', 'ne': '<>', 'l': 'LIKE',
                                'nl': 'NOT LIKE', 'in': 'IN', 'nin': 'NOT IN', 'nn': 'IS NOT'}

    """
  Begin Transactions
"""

    def beginTransaction(self):
        self.begin_transaction = True

    """
  Close Transactions
"""

    def closeTransaction(self):
        self.begin_transaction = False
        self.connection.commit()

    """
  Set Table Name to One Instance
  @type table_name: str
  @param table_name: Table Name
"""

    def setTableName(self, table_name):
        if table_name is not None or table_name != "":
            self.table_name = table_name

    """
  Operator Filter
  @type column: str
  @param column: column name
  @type value_obj: dict
  @param value_obj: like {'eq': 1}, {'gte': 234}, etc...
  @returns str
"""

    def __clauseFilter(self, column, value_obj):
        retrun_str = '{} {} {}'

        for k in value_obj.keys():
            if k == 'table':
                column = value_obj[k]
            elif k == 'col':
                column = '`{}`.`{}`'.format(column, value_obj[k])
            elif k == 'value':
                for j in value_obj[k]:
                    if j in self.clause_operator:
                        if j == 'l' or j == 'nl':
                            value = '"%{}%"'.format(value_obj[k][j])

                        retrun_str = retrun_str.format(column, self.clause_operator[j], value)
                    else:
                        retrun_str = retrun_str.format(column, "=", value)
            else:
                value = value_obj[k]
                if k in self.clause_operator:
                    if k == 'l' or k == 'nl':
                        value = '"%{}%"'.format(value_obj[k])

                    retrun_str = retrun_str.format(column, self.clause_operator[k], value)
                else:
                    retrun_str = retrun_str.format(column, "=", value)

        return retrun_str

    """
  Clause prepare
  @type filter: dict
  @param filter: value pair object like { 'OBJ1': 'VAL1', 'OBJ2': 'VAL2', .... }
  @type c_type: string
  @param c_type: 'AND' | 'OR', Default: 'AND'
  @returns str
"""

    def __clause(self, filter, c_type='AND'):
        clause = ''
        for k in filter.keys():
            if clause != '':
                clause = clause + " {} ".format(c_type)

            if type(filter[k]) is dict:
                clause = clause + self.__clauseFilter(k, filter[k])
            else:
                clause = clause + '{} = {}'.format(k, filter[k])

        return clause

    """
  Perpare Where Clause of the Query
  @type filters: dict
  @param filters: value pair object like { 'and': {'OBJ1': 'VAL1', 'OBJ2': 'VAL2', ....}, 'or': {'OBJ1': 'VAL1', 'OBJ2': 'VAL2', ....}, 'OBJ1': 'VAL1', 'OBJ2': 'VAL2', .... }
  @returns str
"""

    def _prepareWhereClause(self, filters):
        where = ''
        where_or = ''
        where_and = ''
        where_ex = {}

        if filters is not None:
            for k in filters.keys():
                if k.upper() != 'or'.upper() and k.upper() != 'and'.upper():
                    where_ex[k] = filters[k]

            if 'or' in filters:
                where_or = self.__clause(filters['or'], c_type='OR')
            elif 'OR' in filters:
                where_or = self.__clause(filters['OR'], c_type='OR')
            elif 'oR' in filters:
                where_or = self.__clause(filters['oR'], c_type='OR')
            elif 'Or' in filters:
                where_or = self.__clause(filters['Or'], c_type='OR')

            if 'and' in filters:
                where_and = self.__clause(filters['and'])
            elif 'AND' in filters:
                where_and = self.__clause(filters['AND'])
            elif 'And' in filters:
                where_and = self.__clause(filters['And'])
            elif 'aNd' in filters:
                where_and = self.__clause(filters['aNd'])
            elif 'anD' in filters:
                where_and = self.__clause(filters['anD'])
            elif 'ANd' in filters:
                where_and = self.__clause(filters['ANd'])
            elif 'aND' in filters:
                where_and = self.__clause(filters['aND'])
            elif 'AnD' in filters:
                where_and = self.__clause(filters['AnD'])

            if len(where_ex.keys()) > 0:
                if where_and != '':
                    where_and = where_and + ' AND ' + self.__clause(where_ex)
                else:
                    where_and = self.__clause(where_ex)

            if where_or != '' and where_and != '':
                where = '({}) AND {}'.format(where_or, where_and)
            elif where_or != '' and where_and == '':
                where = where_or
            elif where_and != '' and where_or == '':
                where = where_and

        return where

    """
  Sort Order Clause
  @type order_by: dict
  @param order_by: value pair object like { 'OBJ1': 'VAL1', 'OBJ2': 'VAL2', .... }
  @returns str
"""

    def _prepareOrderBy(self, order_by):
        sort_order = ''
        for k in order_by.keys():
            if sort_order != '':
                sort_order = sort_order + ', '
            sort_order = sort_order + '{} {}'.format(k, order_by[k])

        return sort_order

    """
  Count data in table

  @type count_coloum: str
  @param count_coloum: Coloum/s which are counted
  @type where_clause: str
  @param where_clause: Condition on which is executed to count coloum
  @rtype: int
  @returns: return count based on given where_clause and count_coloum
"""

    def countAll(self, count_coloum="*", where_clause=None, group_by=None):
        returnVal = 0
        query = 'SELECT COUNT(' + count_coloum + ') AS `cout` FROM ' + self.database_name + '.' + self.table_name

        if where_clause is not None:
            if type(where_clause) is dict:
                where_clause = self._prepareWhereClause(where_clause)
            query = query + ' WHERE ' + where_clause

        if group_by is not None and group_by != "":
            query = query + ' GROUP BY ' + group_by

        try:
            print("Query",query, '\n\n')
            cur = self.connection.cursor()
            cur.execute(query)
            fetchData = cur.fetchone()

            if fetchData is not None:
                returnVal = fetchData['cout']

            cur.close()
            return returnVal
        except Exception as e:
            return e.__class__.__str__(e)

    """
  Get table data

  @type select_coloum: str
  @param select_coloum: Coloum/s which are returned
  @type where_clause: str
  @param where_clause: Condition on which is executed on coloum
  @type limit: int
  @param limit: How many number of rows returned
  @type page: int
  @param page: Current view page
  @type order_by: string | dict
  @param order_by: Order by clause
  @rtype: list
  @returns: return row list, based on given where_clause and count_coloum
"""

    def selectAll(self, select_column="*", where_clause=None, limit=10, page=1, order_by=None, group_by=None):
        output = None
        #query = 'SELECT ' + select_column + ' FROM ' + self.database_name + '.' + self.table_name
        query = 'SELECT ' + select_column + ' FROM '  + self.table_name

        if where_clause is not None:
            if type(where_clause) is dict:
                where_clause = self._prepareWhereClause(where_clause)

            query = query + ' WHERE ' + where_clause

        if group_by is not None and group_by != "":
            query = query + ' GROUP BY ' + group_by

        if order_by is not None:
            if type(order_by) is dict:
                order_by = self._prepareOrderBy(order_by)
            query = query + ' ORDER BY ' + order_by

        if int(limit) > 0:
            query = query + ' LIMIT ' + str(limit)

        if page > 1:
            page = page - 1
            query = query + ' OFFSET {}'.format(page * int(limit))

        try:
            cur = self.connection.cursor()
            #if self.table_name == 'toc_vessel_details' or self.table_name == 'toc_vessel_detail_list' or self.table_name == 'toc_cargo_term_detailsx':
            # exit()
            print("*** query", query,'\n\n')
            cur.execute(query)

            if cur is not None:
                output = cur.fetchall()
                cur.close()
                return output
            else:
                return output

        except Exception as e:
            return e.__class__.__str__(e)

    """
  Get single row from table

  @type select_coloum: str
  @param select_coloum: Coloum/s which are returned
  @type where_clause: str
  @param where_clause: Condition on which is executed on coloum
  @rtype: dict
  @returns: row dict, based on given where_clause and count_coloum
"""

    def fetchById(self, id, key_name='id', select_coloum="*", where_clause=None, order_by=None, single_row=True):
        output = None
        query = 'SELECT ' + select_coloum + ' FROM ' + self.database_name + '.' + self.table_name

        if where_clause is None:
            query = query + " WHERE " + key_name + " = '" + str(id) + "'"
           
        else:
            if type(where_clause) is dict:
                where_clause = self._prepareWhereClause(where_clause)
            query = query + ' WHERE ' + where_clause + ' AND ' + key_name + ' = "' + str(id) + '"'
        if order_by is not None:
            if type(order_by) is dict:
                order_by = self._prepareOrderBy(order_by)
            query = query + ' ORDER BY ' + order_by

        try:
            cur = self.connection.cursor()
            #if self.table_name == 'toc_user' or self.table_name == 'toc_tcov_full_estimates' :

            print("**** fetech query", query,'\n\n')
            cur.execute(query)

            if cur is not None and single_row == True:
                _output = cur.fetchall()
                if len(_output) > 0:
                    output = _output[0]
                else:
                    output = None
            elif cur is not None and single_row == False:
                output = cur.fetchall()

            cur.close()
            return output
        except Exception as e:
            if "EOF" in e.__class__.__str__(e):
                return None

            return e.__class__.__str__(e)

    def __insertRow(self, cursor, row_data, rel_data=None):
        keys = None
        data = None

        query = "INSERT INTO " + self.database_name + "." + self.table_name

        if rel_data is not None and type(rel_data) is dict:
            for rd in rel_data.keys():
                row_data[rd] = rel_data[rd]

        for key in row_data:
            if keys is not None and data is not None:
                keys = keys + ","
                data = data + ","
            else:
                keys = ""
                data = ""

            keys = keys + "`" + key + "`"
            if (isinstance(row_data[key], str) == True and row_data[key].find('{') >= 0 and row_data[key].find('}') >= 0) or (
                    isinstance(row_data[key], str) == True and row_data[key].find('[') >= 0 and row_data[key].find(']') >= 0):
                data = data + "'{}'".format(row_data[key])
            else:
                data = data + '"{}"'.format(row_data[key])

        query = query + "(" + keys + ") VALUES (" + data + ")"
        # print('in ######################')
        # print(keys)
        # if self.table_name == 'toc_laytime_calculation_other_details' or self.table_name == 'xxx': # or self.table_name == 'toc_voyage_relet_cargos'  :
        print("QueryINS#",query, '\n\n')
            # exit()
        cursor.execute(query)

        return cursor.lastrowid

    """
  Save row of the table

  @type insert_val: dict
  @param insert_val: {ColoumName1:ColoumData1,ColoumName2:ColoumData2}
  @type rel_data: dict | None
  @param rel_data: None | {ColoumName1:ColoumData1,ColoumName2:ColoumData2}

  @rtype: int
  @returns: Insert one row and return it's ID
"""

    def saveData(self, insert_val=dict({}), rel_data=None):
        try:
            cur = self.connection.cursor()
            insert_id = None
            if type(insert_val) is dict:
                insert_id = self.__insertRow(cur, insert_val, rel_data)
            elif type(insert_val) is list:
                insert_id = []
                for r in insert_val:
                    insert_id.append(self.__insertRow(cur, r, rel_data))

            if self.begin_transaction == False:
                self.connection.commit()

            cur.close()
            return insert_id
        except Exception as e:
            # print(insert_val)
            # print(rel_data)
            return e.__class__.__str__(e)

    """
  Update row of the table

  @type where_clause: str
  @param where_clause: Condition on which is executed on coloum
  @type update_val: dict
  @param update_val: {ColoumName1:ColoumData1,ColoumName2:ColoumData2}
  @rtype: int
  @returns: Update one/multiple row and return update count
"""

    def updateData(self, where_clause, update_val=dict({}), filter=None):
        
        data = None
        query = "UPDATE " + self.database_name + "." + self.table_name

        for key in update_val:
            if update_val[key] is not None:
                if data is not None:
                    data = data + ", `" + key + "` = '{}'".format(update_val[key])
                else:
                    data = "`" + key + "` = '{}'".format(update_val[key])

        query = query + " SET " + data
        if filter is not None:
            query = query + " WHERE " + self._prepareWhereClause(filter) + " AND " + where_clause
        else:
            if isinstance(where_clause, dict) == True:
                query = query + " WHERE " + self._prepareWhereClause(where_clause)
            else:
                query = query + " WHERE " + where_clause

        try:
            cur = self.connection.cursor()
            print("QueryUPD#",query, '\n\n')

            # exit;
            # print("query",query)
            cur.execute(query)
            update_count = cur.rowcount

            if self.begin_transaction == False:
                self.connection.commit()

            cur.close()
            return update_count
        except Exception as e:
            return e.__class__.__str__(e)

    """
  Soft Delete row from the table

  @type where_clause: str
  @param where_clause: Condition on which is executed on coloum
  @type set_clause: str
  @param set_clause: `ColoumName1`='ColoumData1',`ColoumName2`='ColoumData2'
  @rtype: int
  @returns: Delete one/multiple row and return delete count
"""

    def deleteData(self, where_clause, set_clause, filter=None):
        query = "UPDATE " + self.database_name + "." + self.table_name

        # print(set_clause)

        query = query + " SET " + set_clause
        if filter is not None and 'where' in filter:
            query = query + " WHERE " + self._prepareWhereClause(filter) + " AND " + where_clause
        else:
            query = query + " WHERE " + where_clause

        try:
            cur = self.connection.cursor()
            print("Query",query)

            cur.execute(query)

            delete_count = cur.rowcount
            self.connection.commit()
            cur.close()
            return delete_count
        except Exception as e:
            return e.__class__.__str__(e)

    def deleteRecord(self, where_clause, filter=None):
        query = "DELETE FROM " + self.database_name + "." + self.table_name

        if filter is not None and 'where' in filter:
            query = query + " WHERE " + self._prepareWhereClause(filter) + " AND " + where_clause
        else:
            query = query + " WHERE " + where_clause

        try:
            cur = self.connection.cursor()
            print("Query DELETE# ",query)

            cur.execute(query)

            delete_count = cur.rowcount
            self.connection.commit()
            cur.close()
            return delete_count
        except Exception as e:
            return e.__class__.__str__(e)


def get_db_connection():
    if 'db_host_lookup' in g and g.db_name_lookup is not None:
        return pymysql.connect(host=g.db_host_lookup, database=g.db_name_lookup, port=g.db_port_lookup,
                               user=g.db_user_lookup,
                               password=g.db_passwd_lookup, cursorclass=pymysql.cursors.DictCursor)
    else:
        # return pymysql.connect(host=os.environ.get("DB_HOST"), database=os.environ.get("DB_NAME"),
        #                        port=int(os.environ.get("DB_PORT")), user=os.environ.get("DB_USER"),
        #                        password=os.environ.get("DB_PASSWORD"), cursorclass=pymysql.cursors.DictCursor)
       
        # return pymysql.connect(host="tocbasedb.cc9zwts1ypfs.ap-southeast-1.rds.amazonaws.com", database="productiondb",
        #                        port=3306, user="productiondb",
        #                        password="$1mtrad8", cursorclass=pymysql.cursors.DictCursor)
       
        # return pymysql.connect(host="db4free.net", database="testdb25",
        #                        port=3306, user="testdb25",
        #                        password="lobhik123", cursorclass=pymysql.cursors.DictCursor)
        return pymysql.connect(host="my-db-instance.cyarommd9bcr.eu-north-1.rds.amazonaws.com", database="initial_db",
                               port=3306, user="lobhik",
                               password="lobhikjuware", cursorclass=pymysql.cursors.DictCursor)

