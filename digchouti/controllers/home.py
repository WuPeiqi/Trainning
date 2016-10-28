#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import json
import hashlib
import time
import copy
import datetime
import collections
from backend.utils.pager import Pagination
from backend.core.request_handler import BaseRequestHandler
from backend import commons
from forms.home import IndexForm
from forms.home import CommentForm
from models import chouti_orm as ORM
from backend.utils import decrator
from backend.utils.response import BaseResponse
from backend.utils.response import StatusCodeEnum
from sqlalchemy import and_, or_


class IndexHandler(BaseRequestHandler):
    def get(self, page=1):

        conn = ORM.session()

        all_count = conn.query(ORM.News).count()

        obj = Pagination(page, all_count)

        current_user_id = self.session['user_info']['nid'] if self.session['is_login'] else 0
        result = conn.query(ORM.News.nid,
                            ORM.News.title,
                            ORM.News.url,
                            ORM.News.content,
                            ORM.News.ctime,
                            ORM.UserInfo.username,
                            ORM.NewsType.caption,
                            ORM.News.favor_count,
                            ORM.News.comment_count,
                            ORM.Favor.nid.label('has_favor')).join(ORM.NewsType, isouter=True).join(ORM.UserInfo, isouter=True).join(ORM.Favor, and_(ORM.Favor.user_info_id == current_user_id, ORM.News.nid == ORM.Favor.news_id), isouter=True)[obj.start:10]
        conn.close()

        str_page = obj.string_pager('/index/')

        self.render('home/index.html', str_page=str_page, news_list=result)

    @decrator.auth_login_json
    def post(self, *args, **kwargs):
        rep = BaseResponse()

        form = IndexForm()
        if form.valid(self):
            # title,content,href,news_type,user_info_id

            input_dict = copy.deepcopy(form._value_dict)
            input_dict['ctime'] = datetime.datetime.now()
            input_dict['user_info_id'] = self.session['user_info']['nid']
            conn = ORM.session()
            conn.add(ORM.News(**input_dict))
            conn.commit()
            conn.close()
            rep.status = True
        else:
            rep.message = form._error_dict

        self.write(json.dumps(rep.__dict__))


class UploadImageHandler(BaseRequestHandler):
    @decrator.auth_login_json
    def post(self, *args, **kwargs):
        rep = BaseResponse()
        try:
            file_metas = self.request.files["img"]
            for meta in file_metas:
                file_name = meta['filename']
                file_path = os.path.join('statics', 'upload', commons.generate_md5(file_name))
                with open(file_path, 'wb') as up:
                    up.write(meta['body'])
            rep.status = True
            rep.data = file_path
        except Exception as ex:
            rep.summary = str(ex)
        self.write(json.dumps(rep.__dict__))


class CommentHandler(BaseRequestHandler):
    def get(self, *args, **kwargs):
        # comment_list需要按照时间从小到大排列
        nid = self.get_argument('nid', 0)
        conn = ORM.session()
        comment_list = conn.query(
            ORM.Comment.nid,
            ORM.Comment.content,
            ORM.Comment.reply_id,
            ORM.UserInfo.username,
            ORM.Comment.ctime,
            ORM.Comment.up,
            ORM.Comment.down,
            ORM.Comment.news_id
        ).join(ORM.UserInfo, isouter=True).filter(ORM.Comment.news_id == nid).all()

        conn.close()
        """
        comment_list = [
            (1, '111',None),
            (2, '222',None),
            (3, '33',None),
            (9, '999',5),
            (4, '444',2),
            (5, '555',1),
            (6, '666',4),
            (7, '777',2),
            (8, '888',4),
        ]
        """

        comment_tree = commons.build_tree(comment_list)

        self.render('include/comment.html', comment_tree=comment_tree)


    @decrator.auth_login_json
    def post(self, *args, **kwargs):
        rep = BaseResponse()

        form = CommentForm()

        if form.valid(self):
            form._value_dict['ctime'] = datetime.datetime.now()

            conn = ORM.session()
            obj = ORM.Comment(user_info_id=self.session['user_info']['nid'],
                              news_id=form._value_dict['news_id'],
                              reply_id=form._value_dict['reply_id'],
                              content=form._value_dict['content'],
                              up=0,
                              down=0,
                              ctime=datetime.datetime.now())

            conn.add(obj)
            conn.flush()
            conn.refresh(obj)

            rep.data = {
                'user_info_id': self.session['user_info']['nid'],
                'username': self.session['user_info']['username'],
                'nid': obj.nid,
                'news_id': obj.news_id,
                'ctime': obj.ctime.strftime("%Y-%m-%d %H:%M:%S"),
                'reply_id': obj.reply_id,
                'content': obj.content,
            }

            conn.query(ORM.News).filter(ORM.News.nid == form._value_dict['news_id']).update(
                {"comment_count": ORM.News.comment_count + 1}, synchronize_session="evaluate")
            conn.commit()
            conn.close()

            rep.status = True
        else:
            rep.message = form._error_dict
        print(rep.__dict__)
        self.write(json.dumps(rep.__dict__))


class FavorHandler(BaseRequestHandler):

    @decrator.auth_login_json
    def post(self, *args, **kwargs):
        rep = BaseResponse()

        news_id = self.get_argument('news_id', None)
        if not news_id:
            rep.summary = "新闻ID不能为空."
        else:
            user_info_id = self.session['user_info']['nid']
            conn = ORM.session()
            has_favor = conn.query(ORM.Favor).filter(ORM.Favor.user_info_id == user_info_id,
                                                     ORM.Favor.news_id == news_id).count()
            if has_favor:
                conn.query(ORM.Favor).filter(ORM.Favor.user_info_id == user_info_id,
                                             ORM.Favor.news_id == news_id).delete()
                conn.query(ORM.News).filter(ORM.News.nid == news_id).update(
                    {"favor_count": ORM.News.favor_count - 1}, synchronize_session="evaluate")
                rep.code = StatusCodeEnum.FavorMinus
            else:
                conn.add(ORM.Favor(user_info_id=user_info_id, news_id=news_id, ctime=datetime.datetime.now()))
                conn.query(ORM.News).filter(ORM.News.nid == news_id).update(
                    {"favor_count": ORM.News.favor_count + 1}, synchronize_session="evaluate")
                rep.code = StatusCodeEnum.FavorPlus
            conn.commit()
            conn.close()

            rep.status = True

        self.write(json.dumps(rep.__dict__))