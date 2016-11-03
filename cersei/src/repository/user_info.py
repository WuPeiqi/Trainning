#!/usr/bin/env python
# -*- coding:utf-8 -*-
from src.utils.db_connection import DbConnection


class UserInfoRepository:
    def __init__(self):
        self.db_conn = DbConnection()

    def add(self, **kwargs):
        cursor = self.db_conn.connect()
        sql = """ insert into user_info(%s) values(%s)"""
        key_list = []
        value_list = []
        for k, v in kwargs.items():
            key_list.append(k)
            value_list.append('%%(%s)s' % k)
        sql = sql % (','.join(key_list), ','.join(value_list))
        cursor.execute(sql, kwargs)
        self.db_conn.close()

    def fetch_by_user_pwd(self, username, password):
        """
        根据用户名密码获取账户信息
        :param username:
        :param password:
        :return:
        """
        cursor = self.db_conn.connect()
        sql = """
          select
            user_info.nid as nid,
            user_info.username as username,
            user_info. user_type_id as user_type_id,
            user_type.caption as user_type_caption
          from
            user_info
          left join user_type on user_info.user_type_id=user_type.nid
          where
            user_info.username=%s and user_info.password=%s
        """
        cursor.execute(sql, [username, password, ])
        result = cursor.fetchone()
        self.db_conn.close()
        return result
