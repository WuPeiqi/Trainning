#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
import hashlib


def fetch_file_md5(file_path):
    obj = hashlib.md5()
    f = open(file_path, 'rb')
    while True:
        b = f.read(8096)
        if not b:
            break
        obj.update(b)
    f.close()
    return obj.hexdigest()


def bar(num=1, total=100):
    rate = float(num) / float(total)
    rate_num = int(rate * 100)
    temp = '\r%d %%' % (rate_num, )
    sys.stdout.write(temp)
    sys.stdout.flush()
