#!/usr/bin/env python
# -*- coding:utf-8 -*-
import pymysql
import Config


class DbConnection:

    def __init__(self):
        self.__conn_dict = Config.PY_MYSQL_CONN_DICT
        self.conn = None
        self.cursor = None

    def connect(self, cursor=pymysql.cursors.DictCursor):
        self.conn = pymysql.connect(**self.__conn_dict)
        self.cursor = self.conn.cursor(cursor=cursor)
        return self.cursor

    def close(self):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()


class UserInfoDao:

    def __init__(self):
        self.db_conn = DbConnection()

    def fetch_single_by_nid(self, nid):
        cursor = self.db_conn.connect()
        sql = "select nid,username from UserInfo where nid = %s"
        cursor.execute(sql, (nid,))
        result = cursor.fetchone()
        self.db_conn.close()
        return result

    def fetch_single_by_user_pwd(self, user, pwd):
        cursor = self.db_conn.connect()
        sql = "select nid,username from UserInfo where username = %s and password = %s"
        cursor.execute(sql, (user,pwd))
        result = cursor.fetchall()
        self.db_conn.close()
        return result

    def fetch_all(self):
        cursor = self.db_conn.connect()
        sql = "select nid,username from UserInfo"
        cursor.execute(sql)
        result = cursor.fetchall()
        self.db_conn.close()
        return result


class NewsDao:

    def __init__(self):
        self.db_conn = DbConnection()

    def fetch_single(self):
        pass

    def fetch_all(self):
        pass

    def fetch_all_join_type(self):
        cursor = self.db_conn.connect()
        sql = "select nid,username from News LEFT JOIN NewsType ON News.type_id = NewsType.nid"
        cursor.execute(sql)
        result = cursor.fetchall()
        self.db_conn.close()
        return result