#!/usr/bin/env python
# -*- coding:utf-8 -*-


import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr


def email(email_list, content, subject="抽屉新热榜-用户注册"):
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['From'] = formataddr(["抽屉新热榜",'wptawy@126.com'])
    msg['Subject'] = subject

    server = smtplib.SMTP("smtp.126.com", 25)
    server.login("wptawy@126.com", "JUEmimima")
    server.sendmail('wptawy@126.com', email_list, msg.as_string())
    server.quit()

