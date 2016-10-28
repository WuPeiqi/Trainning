#!/usr/bin/env python
# -*- coding:utf-8 -*-
import io
import datetime
import json
from backend.utils import check_code
from backend.core.request_handler import BaseRequestHandler
from forms import account
from backend.utils.response import BaseResponse
from backend import commons
from models import chouti_orm as ORM
from sqlalchemy import and_, or_


class CheckCodeHandler(BaseRequestHandler):
    def get(self, *args, **kwargs):
        stream = io.BytesIO()
        img, code = check_code.create_validate_code()
        img.save(stream, "png")
        self.session["CheckCode"] = code
        self.write(stream.getvalue())


class LoginHandler(BaseRequestHandler):
    def post(self, *args, **kwargs):
        rep = BaseResponse()
        form = account.LoginForm()
        if form.valid(self):
            if form._value_dict['code'].lower() != self.session["CheckCode"].lower():
                rep.message = {'code': '验证码错误'}
                self.write(json.dumps(rep.__dict__))
                return
            conn = ORM.session()
            obj = conn.query(ORM.UserInfo).filter(
                or_(
                    and_(ORM.UserInfo.email == form._value_dict['user'],
                         ORM.UserInfo.password == form._value_dict['pwd']),
                    and_(ORM.UserInfo.username == form._value_dict['user'],
                         ORM.UserInfo.password == form._value_dict['pwd'])
                )).first()
            conn.close()
            if not obj:
                rep.message = {'user': '用户名邮箱或密码错误'}
                self.write(json.dumps(rep.__dict__))
                return

            self.session['is_login'] = True
            self.session['user_info'] = obj.__dict__
            rep.status = True
        else:
            rep.message = form._error_dict
        self.write(json.dumps(rep.__dict__))


class RegisterHandler(BaseRequestHandler):
    def post(self, *args, **kwargs):
        rep = BaseResponse()
        form = account.RegisterForm()
        if form.valid(self):
            current_date = datetime.datetime.now()
            limit_day = current_date - datetime.timedelta(minutes=1)
            conn = ORM.session()
            is_valid_code = conn.query(ORM.SendMsg).filter(ORM.SendMsg.email == form._value_dict['email'],
                                                           ORM.SendMsg.code == form._value_dict['email_code'],
                                                           ORM.SendMsg.ctime > limit_day).count()
            if not is_valid_code:
                rep.message['email_code'] = '邮箱验证码不正确或过期'
                self.write(json.dumps(rep.__dict__))
                return
            has_exists_email = conn.query(ORM.UserInfo).filter(ORM.UserInfo.email == form._value_dict['email']).count()
            if has_exists_email:
                rep.message['email'] = '邮箱已经存在'
                self.write(json.dumps(rep.__dict__))
                return
            has_exists_username = conn.query(ORM.UserInfo).filter(
                ORM.UserInfo.username == form._value_dict['username']).count()
            if has_exists_username:
                rep.message['email'] = '用户名已经存在'
                self.write(json.dumps(rep.__dict__))
                return
            form._value_dict['ctime'] = current_date
            form._value_dict.pop('email_code')
            obj = ORM.UserInfo(**form._value_dict)

            conn.add(obj)
            conn.flush()
            conn.refresh(obj)

            user_info_dict = {'nid': obj.nid, 'email': obj.email, 'username': obj.username}

            conn.query(ORM.SendMsg).filter_by(email=form._value_dict['email']).delete()
            conn.commit()
            conn.close()

            self.session['is_login'] = True
            self.session['user_info'] = user_info_dict
            rep.status = True

        else:
            rep.message = form._error_dict

        self.write(json.dumps(rep.__dict__))


class SendMsgHandler(BaseRequestHandler):
    def post(self, *args, **kwargs):
        rep = BaseResponse()
        form = account.SendMsgForm()
        if form.valid(self):
            email = form._value_dict['email']
            conn = ORM.session()

            has_exists_email = conn.query(ORM.UserInfo).filter(ORM.UserInfo.email == form._value_dict['email']).count()
            if has_exists_email:
                rep.summary = "此邮箱已经被注册"
                self.write(json.dumps(rep.__dict__))
                return
            current_date = datetime.datetime.now()
            code = commons.random_code()

            count = conn.query(ORM.SendMsg).filter_by(**form._value_dict).count()
            if not count:
                insert = ORM.SendMsg(code=code,
                                     email=email,
                                     ctime=current_date)
                conn.add(insert)
                conn.commit()
                rep.status = True
            else:
                limit_day = current_date - datetime.timedelta(hours=1)
                times = conn.query(ORM.SendMsg).filter(ORM.SendMsg.email == email,
                                                       ORM.SendMsg.ctime > limit_day,
                                                       ORM.SendMsg.times >= 10,
                                                       ).count()
                if times:
                    rep.summary = "'已经超过今日最大次数（1小时后重试）'"
                else:
                    unfreeze = conn.query(ORM.SendMsg).filter(ORM.SendMsg.email == email,
                                                              ORM.SendMsg.ctime < limit_day).count()
                    if unfreeze:
                        conn.query(ORM.SendMsg).filter_by(email=email).update({"times": 0})

                    conn.query(ORM.SendMsg).filter_by(email=email).update({"times": ORM.SendMsg.times + 1,
                                                                           "code": code,
                                                                           "ctime": current_date},
                                                                          synchronize_session="evaluate")
                    conn.commit()
                    rep.status = True
            conn.close()
        else:
            rep.summary = form._error_dict['email']
        self.write(json.dumps(rep.__dict__))

