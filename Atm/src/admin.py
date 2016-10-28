#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import json
from lib import commons
from config import settings

CURRENT_USER_INFO = {'is_authenticated': False, 'current_user': None}


def init():
    """
    初始化管理员信息
    :return:
    """
    dic = {'username': 'alex', 'password': commons.md5('123')}

    json.dump(dic, open(os.path.join(settings.ADMIN_DIR_FOLDER, dic['username']), 'w'))


def create_user():
    """
    创建账户
    :return:
    """
    card_num = "6222020409028810"

    os.makedirs(os.path.join(settings.USER_DIR_FOLDER, card_num, 'record'))

    base_info = {'username': 'rain',
                 'card': card_num,
                 'password': commons.md5('8888'),
                 "credit": 15000,  # 信用卡额度
                 "balance": 15000, # 本月可用额度
                 "saving": 0,      # 储蓄金额
                 "enroll_date": "2016-01-01",
                 'expire_date': '2021-01-01',
                 'status': 0,  # 0 = normal, 1 = locked, 2 = disabled
                 "debt": [], # 欠款记录，如：
                 # [
                 # {'date': "2015_4_10", "total_debt":80000, "balance_debt": 5000},
                 # {'date': "2015_5_10", "total":80000, "balance": 5000}
                 # ]
                 }

    json.dump(base_info, open(os.path.join(settings.USER_DIR_FOLDER, card_num, "basic_info.json"), 'w'))


def remove_user():
    """
    移除账户
    :return:
    """
    pass


def locked_user():
    """
    冻结账户
    :return:
    """
    pass


def search():
    """
    搜索账户
    :return:
    """
    pass


def main():

    menu = """
    1、创建账户；
    2、删除账户；
    3、冻结账户；
    4、查询账户
    """
    print(menu)
    menu_dic = {
        '1': create_user,
        '2': remove_user,
        '3': locked_user,
        '4': search,
    }

    while True:
        user_option = input(">>:").strip()
        if user_option in menu_dic:
            menu_dic[user_option]()

        else:
            print("选项不存在")


def login():
    """
    用户登陆
    :return:
    """
    while True:
        username = input('请输入用户名：')
        password = input('请输入密码：')

        if not os.path.exists(os.path.join(settings.ADMIN_DIR_FOLDER, username)):
            print('用户名不存在')
        else:
            user_dict = json.load(open(os.path.join(settings.ADMIN_DIR_FOLDER, username), 'r'))
            if username == user_dict['username'] and commons.md5(password) == user_dict['password']:
                CURRENT_USER_INFO['is_authenticated'] = True
                CURRENT_USER_INFO['current_user'] = username
                return True
            else:
                print('密码错误')


def run():
    ret = login()
    if ret:
        main()



