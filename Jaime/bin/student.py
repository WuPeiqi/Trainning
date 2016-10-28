#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import sys

BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.path.join(BASEDIR)


r = os.listdir(BASEDIR)
print(r)

import uuid


r = uuid.uuid1()
print(r,type(r),len(str(r)))