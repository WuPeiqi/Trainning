#!/usr/bin/env python
# -*- coding:utf-8 -*-
from Dao import PyORM


class UserInfoDaoFactory:

    __dao = PyORM.UserInfoDao()

    @staticmethod
    def set_dao(dao):
        UserInfoDaoFactory.__dao = dao

    @staticmethod
    def get_dao():
        return UserInfoDaoFactory.__dao


class NewsDaoFactory:

    __dao = PyORM.NewsDao()

    @staticmethod
    def set_dao(dao):
        NewsDaoFactory.__dao = dao

    @staticmethod
    def get_dao():
        return NewsDaoFactory.__dao
