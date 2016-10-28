#!/usr/bin/env python
# -*- coding:utf-8 -*-


PY_MYSQL_CONN_DICT = {
    "host": '127.0.0.1',
    "port": 3306,
    "user": 'root',
    "passwd": '123',
    "db": 't1'
}

SQL_ALCHEMY_CONN_STR = "mysql+pymysql://root:123@127.0.0.1:3306/t1"

SQL_ALCHEMY_MAX_OVERFLOW = 1