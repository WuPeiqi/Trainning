#!/usr/bin/env python
# -*- coding:utf-8 -*-
from src.utils.db_connection import DbConnection


class UserTypeToPermissionRepository:
    def __init__(self):
        self.db_conn = DbConnection()

    def add(self, **kwargs):
        cursor = self.db_conn.connect()
        sql = """ insert into user_type_to_permission(%s) values(%s)"""
        key_list = []
        value_list = []
        for k, v in kwargs.items():
            key_list.append(k)
            value_list.append('%%(%s)s' % k)
        sql = sql % (','.join(key_list), ','.join(value_list))
        cursor.execute(sql, kwargs)
        self.db_conn.close()

    def fetch_permission_by_type_id(self, user_type_id):
        cursor = self.db_conn.connect()
        sql = """
          select
            permission.nid as nid,
            permission.caption as caption,
            permission.module as module,
            permission.func as func
          from
            user_type_to_permission
          left join permission on user_type_to_permission.permission_id = permission.nid
          where user_type_to_permission.user_type_id = %s
        """
        cursor.execute(sql, user_type_id)
        result = cursor.fetchall()
        self.db_conn.close()
        return result
