#!/usr/bin/python
#-*- coding=utf-8 -*-
import sys
import MySQLdb


class Database:
    host = 'localhost'
    user = 'root'
    password = '123456'
    db = 'weibo_service'

    def __init__(self):
        self.connection = MySQLdb.connect(self.host, self.user, self.password, self.db)
        self.cursor = self.connection.cursor()
        self.cursor.execute("SET NAMES utf8")
        self.cursor.execute("SET CHARACTER_SET_CLIENT=utf8")
        self.cursor.execute("SET CHARACTER_SET_RESULTS=utf8")


    def insert(self,table_name,data):
        columns = data.keys()
        _prefix = "".join(['INSERT INTO `',table_name,'`'])
        _fields = ",".join(["".join(['`',column,'`']) for column in columns])
        _values = ",".join(["%s" for i in range(len(columns))])
        _sql = "".join([_prefix,"(",_fields,") VALUES (",_values,")"])
        _params = [ data[key] for key in columns ]
        # print _sql
        # print _params
        self.cursor.execute(_sql,tuple(_params))
        self.connection.commit()

    def is_key_exist(self,table_name,key_name,key_value):
        
        query_sql = """select * from %s where %s='%s'"""%(table_name, key_name, key_value)
        return self.cursor.execute(query_sql)

    # def test(self):
    #     query_sql = "show tables;"
    #     f = self.cursor.execute(query_sql)
    #     print f 
    def __del__(self):
        self.connection.close()

if __name__ == '__main__':
    db = Database()
    print db.is_key_exist("report_info","rid","K1CaL7ABf7Kgl")