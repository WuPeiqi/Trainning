#!/usr/bin/env python
# -*- coding:utf-8 -*-
from src.repository.user_info import UserInfoRepository
from src.repository.user_type_to_permission import UserTypeToPermissionRepository
from src.utils import commons
from config import settings

import importlib


def choice_menu():
    print('登陆成功：%s' % settings.current_user_info['username'])
    while True:
        for i, item in enumerate(settings.current_user_permission_list, 1):
            print(i, item['caption'])
        choice = input('请输入菜单：')
        choice = int(choice)
        permission = settings.current_user_permission_list[choice - 1]

        module = permission['module']
        func_name = permission['func']

        m = importlib.import_module(module)
        func = getattr(m, func_name)
        func()


def find_pwd():
    pass


def register():
    pass


def login():
    while True:
        username = input('请输入用户名：')
        password = input('请输入用户名：')
        pwd = commons.md5(password)
        user_repository = UserInfoRepository()
        user_info = user_repository.fetch_by_user_pwd(username, pwd)
        if not user_info:
            print('用户名或密码错误，请重新输入.')
            continue
        type_to_per_repository = UserTypeToPermissionRepository()
        permission_list = type_to_per_repository.fetch_permission_by_type_id(user_info['user_type_id'])

        settings.current_user_permission_list = permission_list
        settings.current_user_info = user_info
        return True


def execute():
    while True:
        print('欢迎登陆权限管理系统：1:登陆;2:注册;3:找回密码;\n')
        dic = {
            '1': login,
            '2': register,
            '3': find_pwd,
        }
        choice = input('请输入选项：')
        if choice not in dic.keys():
            print('选项输入错误')
            continue
        func = dic[choice]
        result = func()
        if result:
            choice_menu()
