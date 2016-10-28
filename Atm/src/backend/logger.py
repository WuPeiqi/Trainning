#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import time
import logging
from config import settings


def get_logger(card_num, struct_time):

    if struct_time.tm_mday < 23:
        file_name = "%s_%s_%d" %(struct_time.tm_year, struct_time.tm_mon, 22)
    else:
        file_name = "%s_%s_%d" %(struct_time.tm_year, struct_time.tm_mon+1, 22)

    file_handler = logging.FileHandler(
        os.path.join(settings.USER_DIR_FOLDER, card_num, 'record', file_name),
        encoding='utf-8'
    )
    fmt = logging.Formatter(fmt="%(asctime)s :  %(message)s")
    file_handler.setFormatter(fmt)

    logger1 = logging.Logger('user_logger', level=logging.INFO)
    logger1.addHandler(file_handler)
    return logger1