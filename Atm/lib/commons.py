#!/usr/bin/env python
# -*- coding:utf-8 -*-
import hashlib


def md5(arg):
    """
    md5加密
    :param arg:
    :return:
    """
    obj = hashlib.md5()
    obj.update(bytes(arg, encoding='utf-8'))
    return obj.hexdigest()
