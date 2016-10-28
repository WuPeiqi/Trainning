#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import logging
import time
import json

from config import settings
from src.backend import logger


CURRENT_USER_INFO = {}


def dump_current_user_info():

    json.dump(CURRENT_USER_INFO, open(os.path.join(settings.USER_DIR_FOLDER, CURRENT_USER_INFO['card'], "basic_info.json"), 'w'))


def write_record(message):
    """
    账户记录
    :param message:
    :return:
    """
    struct_time = time.localtime()
    logger_obj = logger.get_logger(CURRENT_USER_INFO['card'], struct_time)
    logger_obj.info(message)


def account_info():
    """
    账户信息
    :return:
    """
    pass


def repay():
    """
    还款
    :return:
    """
    pass


def withdraw():
    """
    提现
    提现时，优先从自己余额中拿，如果余额不足，则使用信用卡（额度限制），提现需要手续费10%
    :return:
    """
    num = float(input('请输入提现金额'))
    if CURRENT_USER_INFO['saving'] >= num:
        CURRENT_USER_INFO['saving'] -= num

        write_record('%s - 储蓄账户：%d' % ("提现", num))
        dump_current_user_info()
    else:
        temp = num - CURRENT_USER_INFO['saving']
        if CURRENT_USER_INFO['balance'] > (temp + temp * 0.05):
            CURRENT_USER_INFO['balance'] -= temp
            CURRENT_USER_INFO['balance'] -= temp * 0.05

            write_record('%s - 储蓄账户：%f；信用卡账户：%f；手续费：%f' % ("提现", CURRENT_USER_INFO['saving'], temp, temp * 0.05))
            dump_current_user_info()
        else:
            print('账户余额不足，无法完成提现')


def transfer():
    """
    转账
    :return:
    """
    pass


def pay_check():
    pass


def main():
    menu = '''
    1.  账户信息
    2.  还款
    3.  取款
    4.  转账
    5.  账单
    '''
    menu_dic = {
        '1': account_info,
        '2': repay,
        '3': withdraw,
        '4': transfer,
        '5': pay_check,
    }
    while True:
        print(menu)
        user_option = input(">>:").strip()
        if user_option in menu_dic:
            menu_dic[user_option]()

        else:
            print("选项不存在")


def init(card):

    basic_info = json.load(open(os.path.join(settings.USER_DIR_FOLDER, card, "basic_info.json")))
    CURRENT_USER_INFO.update(basic_info)


def login():
    """
    登陆
    :return:
    """

    card_num = "6222020409028810"
    if card_num == "6222020409028810":
        init(card_num)

    return True


def run():
    ret = login()
    if ret:
        main()
