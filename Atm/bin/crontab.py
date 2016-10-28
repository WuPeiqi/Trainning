#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
定时任务，每日凌晨 00:00自动执行
"""

from src import crontab as src_crontab


if __name__ == '__main__':
    src_crontab.run()