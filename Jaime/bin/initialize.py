#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    用于初始化管理员账户
"""
from src.service import initialize_service


def execute():

    initialize_service.main()

if __name__ == '__main__':
    execute()
