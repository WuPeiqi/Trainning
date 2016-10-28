#!/usr/bin/env python
# -*- coding:utf-8 -*-

from backend.form.forms import BaseForm
from backend.form.fields import StringField
from backend.form.fields import IntegerField
from backend.form.fields import EmailField


class SendMsgForm(BaseForm):

    def __init__(self):
        self.email = EmailField(custom_error_dict={'required': '注册邮箱不能为空.', 'valid': '注册邮箱格式错误.'})

        super(SendMsgForm, self).__init__()


class RegisterForm(BaseForm):

    def __init__(self):
        self.username = StringField()
        self.email = EmailField()
        self.password = StringField()
        self.email_code = StringField()

        super(RegisterForm, self).__init__()

class LoginForm(BaseForm):

    def __init__(self):
        self.user = StringField()
        self.pwd = StringField()
        self.code = StringField()

        super(LoginForm, self).__init__()