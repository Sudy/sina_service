#!/usr/bin/python
#-*- coding=utf-8 -*-
import sys
import MySQLdb


class Database:
    host = 'localhost'
    user = 'root'
    password = '123456'
    db = 'YLC'

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
        print _sql
        print _params
        # self.cursor.execute(_sql,tuple(_params))
        # self.connection.commit()

    def is_key_exist(self,key_name):
        query_sql = "select * from user where domain = %s"
        return self.cursor.execute(query_sql,tuple(key_name))

    def __del__(self):
        self.connection.close()


if __name__ == "__main__":
    db = Database()
    for line in sys.stdin:
        if line != "":
            weibo_data = line.strip().split("\t",5)
        try:
            query_sql = "insert into weibodata (w_mid,w_content,w_loc,w_time,w_emotion,w_uname)\
            values (%s, %s, %s, %s, %s, %s)"
            #print file_name,weibo_data[1]
            data = (weibo_data[0],weibo_data[1],weibo_data[2],weibo_data[3],weibo_data[4],weibo_data[5])

            #print query_sql
            db.insert(query_sql,data)
        except:
            print weibo_data[0],weibo_data[0]
        continue
