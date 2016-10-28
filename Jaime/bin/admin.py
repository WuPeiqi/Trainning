#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    用于为管理员用户提供相关操作，如：学校、课程、老师等相关操作
"""
from src.service import admin_service


def execute():

    admin_service.main()

if __name__ == '__main__':
    execute()
