#!/usr/bin/env python
# -*- coding:utf-8 -*-
from src.utils.db_connection import DbConnection


class PermissionRepository:
    def __init__(self):
        self.db_conn = DbConnection()

    def add(self, **kwargs):
        cursor = self.db_conn.connect()
        sql = """ insert into permission(%s) values(%s)"""
        key_list = []
        value_list = []
        for k, v in kwargs.items():
            key_list.append(k)
            value_list.append('%%(%s)s' % k)
        sql = sql % (','.join(key_list), ','.join(value_list))
        cursor.execute(sql, kwargs)
        self.db_conn.close()

    def fetch_all(self):
        cursor = self.db_conn.connect()
        sql = """
          select
            nid,
            caption,
            module,
            func
          from
            permission
        """
        cursor.execute(sql)
        result = cursor.fetchall()
        self.db_conn.close()
        return result


