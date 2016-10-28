#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django import forms


class IndexForm(forms.Form):

    title = forms.CharField()
    content = forms.CharField(required=False)
    url = forms.CharField(required=False)
    news_type_id = forms.IntegerField()


class CommentForm(forms.Form):
    content = forms.CharField()
    news_id = forms.IntegerField()
    reply_id = forms.IntegerField()
