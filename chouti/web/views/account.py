#!/usr/bin/env python
# -*- coding:utf-8 -*-
import io
import json
import datetime

from django.shortcuts import HttpResponse,redirect,render

from web.forms.account import SendMsgForm,RegisterForm,LoginForm
from web import models

from backend import commons
from backend.utils import check_code as CheckCode
from backend.utils.response import BaseResponse


def check_code(request):
    stream = io.BytesIO()
    img, code = CheckCode.create_validate_code()
    img.save(stream, "png")
    request.session["CheckCode"] = code
    return HttpResponse(stream.getvalue())


def send_msg(request):
    rep = BaseResponse()
    form = SendMsgForm(request.POST)
    if form.is_valid():
        _value_dict = form.clean()
        email = _value_dict['email']

        has_exists_email = models.UserInfo.objects.filter(email=email).count()
        if has_exists_email:
            rep.summary = "此邮箱已经被注册"
            return HttpResponse(json.dumps(rep.__dict__))

        current_date = datetime.datetime.now()
        code = commons.random_code()

        count = models.SendMsg.objects.filter(email=email).count()
        if not count:
            models.SendMsg.objects.create(code=code, email=email, ctime=current_date)
            rep.status = True
        else:
            limit_day = current_date - datetime.timedelta(hours=1)

            times = models.SendMsg.objects.filter(email=email, ctime__gt=limit_day, times__gt=9).count()
            if times:
                rep.summary = "'已超最大次数（1小时后重试）'"
            else:
                unfreeze = models.SendMsg.objects.filter(email=email, ctime__lt=limit_day).count()
                if unfreeze:
                    models.SendMsg.objects.filter(email=email).update(times=0)

                from django.db.models import F
                models.SendMsg.objects.filter(email=email).update(code=code,
                                                                  ctime=current_date,
                                                                  times=F('times')+1)
                rep.status = True
    else:

        error_dict = json.loads(form.errors.as_json())

        rep.summary = error_dict['email'][0]['message']
    return HttpResponse(json.dumps(rep.__dict__))


def register(request):
    rep = BaseResponse()
    form = RegisterForm(request.POST)
    if form.is_valid():
        current_date = datetime.datetime.now()
        limit_day = current_date - datetime.timedelta(minutes=1)
        _value_dict = form.clean()

        is_valid_code = models.SendMsg.objects.filter(email=_value_dict['email'],
                                                      code=_value_dict['email_code'],
                                                      ctime__gt=limit_day).count()
        if not is_valid_code:
            rep.message['email_code'] = '邮箱验证码不正确或过期'
            return HttpResponse(json.dumps(rep.__dict__))

        has_exists_email = models.UserInfo.objects.filter(email=_value_dict['email']).count()

        if has_exists_email:
            rep.message['email'] = '邮箱已经存在'
            return HttpResponse(json.dumps(rep.__dict__))

        has_exists_username = models.UserInfo.objects.filter(username=_value_dict['username']).count()
        if has_exists_username:
            rep.message['email'] = '用户名已经存在'
            return HttpResponse(json.dumps(rep.__dict__))

        _value_dict['ctime'] = current_date
        _value_dict.pop('email_code')
        obj = models.UserInfo.objects.create(**_value_dict)

        user_info_dict = {'nid': obj.nid, 'email': obj.email, 'username': obj.username}

        models.SendMsg.objects.filter(email=_value_dict['email']).delete()

        request.session['is_login'] = True
        request.session['user_info'] = user_info_dict
        rep.status = True

    else:
        error_msg = form.errors.as_json()
        rep.message = json.loads(error_msg)
    return HttpResponse(json.dumps(rep.__dict__))


def login(request):

    rep = BaseResponse()
    form = LoginForm(request.POST)
    if form.is_valid():
        _value_dict = form.clean()
        if _value_dict['code'].lower() != request.session["CheckCode"].lower():
            rep.message = {'code':[{'message':'验证码错误'}]}
            return HttpResponse(json.dumps(rep.__dict__))

        from django.db.models import Q
        con = Q()

        q1 = Q()
        q1.connector = 'AND'
        q1.children.append(('email', _value_dict['user']))
        q1.children.append(('password', _value_dict['pwd']))

        q2 = Q()
        q2.connector = 'AND'
        q2.children.append(('username', _value_dict['user']))
        q2.children.append(('password', _value_dict['pwd']))

        con.add(q1, 'OR')
        con.add(q2, 'OR')

        obj = models.UserInfo.objects.filter(con).first()
        if not obj:
            rep.message = {'user': [{'message':'用户名邮箱或密码错误'}]}
            return HttpResponse(json.dumps(rep.__dict__))

        request.session['is_login'] = True
        request.session['user_info'] = {'nid': obj.nid, 'email': obj.email, 'username': obj.username}
        rep.status = True
    else:
        error_msg = form.errors.as_json()
        print(error_msg)
        rep.message = json.loads(error_msg)

    return HttpResponse(json.dumps(rep.__dict__))


def logout(request):

    request.session.clear()
    return redirect('/index/')


def test_request(request):
    from django.http.request import QueryDict
    from django.core.handlers.wsgi import WSGIRequest
    print(request,type(request))
    print(request.POST,type(request.POST))
    v1 = request.POST.getlist('favor_intval')

    v2 = request.POST.get('1')
    print(v1,v2)
    v1 = request.GET.getlist('favor_intval')

    v2 = request.GET.get('1')
    print(v1,v2)
    return render(request, 'test_request.html')