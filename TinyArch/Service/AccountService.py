#!/usr/bin/env python
# -*- coding:utf-8 -*-
from Dao.DaoFacotory import UserInfoDaoFactory
from Dao.DaoFacotory import NewsDaoFactory


def login(username, password):
    user_info_dao = UserInfoDaoFactory.get_dao()
    ret = user_info_dao.fetch_single_by_user_pwd(username, password)
    if ret:
        pass
    else:
        pass


def logout():
    pass


def register():
    pass