#!/usr/bin/env python
# -*- coding:utf-8 -*-
from Dao import PyORM
from Dao import PyMySQL
from Dao import DaoFacotory


def static_mapper():
    DaoFacotory.NewsDaoFactory.set_dao(PyMySQL.UserInfoDao)


def dynamic_mapper(handler):
    pass
