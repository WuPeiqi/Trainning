#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django import forms


class SendMsgForm(forms.Form):

    email = forms.EmailField()


class RegisterForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField()
    email_code = forms.CharField()


class LoginForm(forms.Form):
    user = forms.CharField()
    pwd = forms.CharField()
    code = forms.CharField()

