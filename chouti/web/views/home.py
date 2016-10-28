#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import copy
import datetime
import json

from django.shortcuts import render, HttpResponse
from django.db.models import F


from web import models
from web.forms.home import IndexForm

from backend.utils.pager import Pagination
from backend.utils.response import BaseResponse,StatusCodeEnum
from backend import commons

def index(request):
    # print(request.session['is_login'])
    # print(request.session['user_info'])

    if request.method == 'GET':
        page = request.GET.get('page', 1)
        all_count = models.News.objects.all().count()

        obj = Pagination(page, all_count)

        sql = """
        SELECT
            "web_news"."nid",
            "web_news"."title",
            "web_news"."url",
            "web_news"."content",
            "web_news"."ctime",
            "web_userinfo"."username",
            "web_newstype"."caption",
            "web_news"."favor_count",
            "web_news"."comment_count",
            "web_favor"."nid"
        FROM
            "web_news"
        LEFT OUTER JOIN "web_userinfo" ON (
            "web_news"."user_info_id" = "web_userinfo"."nid"
        )
        LEFT OUTER JOIN "web_newstype" ON (
            "web_news"."news_type_id" = "web_newstype"."nid"
        )
        LEFT OUTER JOIN "web_favor" ON
            "web_news"."nid" = "web_favor"."news_id"
        and
            "web_favor"."user_info_id" = %s

        LIMIT 10 OFFSET %s
        """

        from django.db import connection
        cursor = connection.cursor()
        cursor.execute(sql, [request.session['user_info']['nid'] if request.session.get('user_info', None) else 0, obj.start])
        result = cursor.fetchall()
        str_page = obj.string_pager('/index/')

        return render(request, 'index.html', {'str_page': str_page, 'news_list': result})
    else:
        rep = BaseResponse()

        form = IndexForm(request.POST)
        if form.is_valid():
            # title,content,href,news_type,user_info_id
            _value_dict = form.clean()
            input_dict = copy.deepcopy(_value_dict)
            input_dict['ctime'] = datetime.datetime.now()
            input_dict['user_info_id'] = request.session['user_info']['nid']
            models.News.objects.create(**input_dict)
            rep.status = True
        else:

            error_msg = form.errors.as_json()
            rep.message = json.loads(error_msg)

        return HttpResponse(json.dumps(rep.__dict__))



def favor(request):
    rep = BaseResponse()

    news_id = request.POST.get('news_id', None)
    if not news_id:
        rep.summary = "新闻ID不能为空."
    else:
        user_info_id = request.session['user_info']['nid']

        has_favor = models.Favor.objects.filter(user_info_id=user_info_id, news_id=news_id).count()
        if has_favor:
            models.Favor.objects.filter(user_info_id=user_info_id, news_id=news_id).delete()
            models.News.objects.filter(nid=news_id).update(favor_count=F('favor_count')-1)

            rep.code = StatusCodeEnum.FavorMinus
        else:
            models.Favor.objects.create(user_info_id=user_info_id, news_id=news_id, ctime=datetime.datetime.now())
            models.News.objects.filter(nid=news_id).update(favor_count=F('favor_count')+1)

            rep.code = StatusCodeEnum.FavorPlus

        rep.status = True

    return HttpResponse(json.dumps(rep.__dict__))



def upload_image(request):

    rep = BaseResponse()
    try:
        obj = request.FILES.get('img')
        file_path = os.path.join('statics', 'upload', commons.generate_md5(obj.name))

        f = open(file_path, 'wb')
        for chunk in obj.chunks():
            f.write(chunk)
        f.close()

        rep.status = True
        rep.data = file_path
    except Exception as ex:
        rep.summary = str(ex)
    return HttpResponse(json.dumps(rep.__dict__))