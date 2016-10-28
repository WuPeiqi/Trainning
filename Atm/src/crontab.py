#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import json
import time

from config import settings
from src.backend import logger


def main():
    card_list = os.listdir(settings.USER_DIR_FOLDER)
    for card in card_list:
        basic_info = json.load(open(os.path.join(settings.USER_DIR_FOLDER, card, 'basic_info.json')))
        struct_time = time.localtime()

        # 循环账单列表，为每月的欠款计息。并写入到当月账单中
        for item in basic_info['debt']:
            interest = item['total_debt'] * 0.0005
            if basic_info['saving'] >= interest:
                basic_info['saving'] -= interest
            else:
                temp = interest - basic_info['saving']
                basic_info['balance'] -= temp
            logger_obj = logger.get_logger(card, struct_time)
            logger_obj.info("欠款利息 - %f - 备注：未还款日期%s；共欠款%f，未还款%f" % (interest, item['date'], item['total_debt'], item['balance_debt'],))

            json.dump(
                basic_info,
                open(os.path.join(settings.USER_DIR_FOLDER, basic_info['card'], "basic_info.json"), 'w')
            )

        # 如果当前等于10号(9号之前)
        #   当前余额为负值，则将值添加到账单列表中，开始计息，同时，本月可用额度恢复。
        if struct_time.tm_mday == 11 and basic_info['credit'] > basic_info['balance']:
            date = time.strftime("%Y-%m-%d")
            dic = {'date': date,
                   "total_debt": basic_info['credit'] - basic_info['balance'],
                   "balance_debt": basic_info['credit'] - basic_info['balance'],
                   }
            basic_info['debt'].append(dic)
            # 恢复可用额度
            basic_info['balance'] = basic_info['credit']
            json.dump(
                basic_info,
                open(os.path.join(settings.USER_DIR_FOLDER, basic_info['card'], "basic_info.json"), 'w')
            )


def run():

    main()
