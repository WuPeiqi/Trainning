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
from backend.utils.response import BaseResponse, StatusCodeEnum
from backend import commons


def index(request):
    """
    抽屉主页
    :param request:
    :return:
    """
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
        cursor.execute(sql, [request.session['user_info']['nid'] if request.session.get('user_info', None) else 0,
                             obj.start])
        result = cursor.fetchall()
        str_page = obj.string_pager('/index/')

        return render(request, 'index.html', {'str_page': str_page, 'news_list': result})
    else:
        rep = BaseResponse()
        form = IndexForm(request.POST)
        if form.is_valid():
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
    """
    点赞
    :param request:
    :return:
    """
    rep = BaseResponse()

    news_id = request.POST.get('news_id', None)
    if not news_id:
        rep.summary = "新闻ID不能为空."
    else:
        user_info_id = request.session['user_info']['nid']

        has_favor = models.Favor.objects.filter(user_info_id=user_info_id, news_id=news_id).count()
        if has_favor:
            models.Favor.objects.filter(user_info_id=user_info_id, news_id=news_id).delete()
            models.News.objects.filter(nid=news_id).update(favor_count=F('favor_count') - 1)

            rep.code = StatusCodeEnum.FavorMinus
        else:
            models.Favor.objects.create(user_info_id=user_info_id, news_id=news_id, ctime=datetime.datetime.now())
            models.News.objects.filter(nid=news_id).update(favor_count=F('favor_count') + 1)

            rep.code = StatusCodeEnum.FavorPlus

        rep.status = True

    return HttpResponse(json.dumps(rep.__dict__))


def upload_image(request):
    """
    上传图片
    :param request:
    :return:
    """
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


class CommentNode:
    HTML_TEMPLATE = """
    <div class='content' id="comment_content_%s" style='margin-left:%s;'>
        <span>%s</span>
    """

    def __init__(self, nid, content, reply_id):
        self.nid = nid
        self.content = content
        self.reply_id = reply_id

        self.children = []

    @staticmethod
    def __recursion_convert_tree(result, row_dict):
        for child in result:
            if child.nid == row_dict.get('reply_id'):
                obj = CommentNode(**row_dict)
                child.children.append(obj)
                break
            else:
                CommentNode.__recursion_convert_tree(child.children, row_dict)


    @staticmethod
    def convert_tree(comment_list):
        result = []
        for row_dict in comment_list:
            if not row_dict.get('reply_id', None):
                obj = CommentNode(**row_dict)
                result.append(obj)
            else:
                CommentNode.__recursion_convert_tree(result, row_dict)

        return result


    @staticmethod
    def html_tree(node_list):
        html = '<div class="comment">'
        for node in node_list:
            html += CommentNode.HTML_TEMPLATE % (node.nid, 30, node.content)
            if node.children:
                html += CommentNode.html_tree(node.children)
            html += "</div>"
        html += '</div>'

        return html


def fetch_comment(request):
    """
    点赞
    :param request:
    :return:
    """
    # news_id = request.GET.get('news_id', None)
    # comment_list = models.Comment.objects.filter(news_id = news_id).order_by("ctime")

    comment_list = [
        {'nid': 1, 'content': '我日1', 'reply_id': None},
        {'nid': 2, 'content': '我日2', 'reply_id': None},
        {'nid': 3, 'content': '我日3', 'reply_id': None},
        {'nid': 4, 'content': '我日4', 'reply_id': None},
        {'nid': 5, 'content': '我日5', 'reply_id': None},
        {'nid': 6, 'content': '别闹了', 'reply_id': 1},
        {'nid': 7, 'content': '去你的', 'reply_id': 1},
        {'nid': 8, 'content': '真的吗', 'reply_id': 6},
        {'nid': 9, 'content': '哈哈哈哈哈', 'reply_id': 6},
    ]

    result = CommentNode.convert_tree(comment_list)
    html = CommentNode.html_tree(result)

    return HttpResponse(html)


def add_comment(request):
    import datetime
    import time
    print(1)
    obj = HttpResponse('OK')
    obj.set_cookie('is_login', 'root')
    return obj


def show(request):
    print(request.COOKIES)

    v = request.COOKIES.get('ppppp')
    obj = render(request, 'test.html', {'u': v})
    return obj