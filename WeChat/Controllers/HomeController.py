#!/usr/bin/env python
# -*- coding:utf-8 -*-
import tornado.ioloop
import tornado.web

import time
import requests
import re
import json
import copy
import urllib2

WECHAT_SESSION_ID = None
WECHAT_TIMESPAN = None

FETCH_SESSION_ID_URL = "https://login.weixin.qq.com/jslogin?appid=wx782c26e4c19acffb&redirect_uri=https%3A%2F%2Fwx.qq.com%2Fcgi-bin%2Fmmwebwx-bin%2Fwebwxnewloginpage&fun=new&lang=zh_CN&_={0}"

CHECK_LOGIN_URL = "https://login.weixin.qq.com/cgi-bin/mmwebwx-bin/login?loginicon=true&uuid={0}&tip=0&r=-1356532462&_={1}"

REDIRECT_URL_SUFFIX = '&fun=new&version=v2&lang=zh_CN'

# 获取用户信息
USER_INIT_URL = 'http://wx.qq.com/cgi-bin/mmwebwx-bin/webwxinit?pass_ticket=%s&skey=%s&r=%s'

# https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxinit?r=-457597863&lang=zh_CN&pass_ticket=4417Iocth3MSkUbvpGXPW1iERw6HoYNzBAuPgaTKYK8OIHdNbz%252BSxxL8BwJ2srBr

CODE_COOKIE_DICT = {}

TICKET_COOKIE_DICT = {}

ALL_COOKIE_DICT = {}

BASE_REQUEST_DICT = {}

TICKET_RESULT_DICT = {}

INIT_RESULT_DICT = {}

CURRENT_USER = {}

USER_LIST_DICT = {}

def urllib2_request(url, param):
    request = urllib2.Request(url=url, data=json.dumps(param))
    request.add_header('ContentType', 'application/json; charset=UTF-8')
    response = urllib2.urlopen(request)
    origin = response.read()
    return origin


class LoginHandler(tornado.web.RequestHandler):

    def get(self):
        """
        获取当前时间戳并向微信发送Http请求，从而获取SessionId，然后根据SessionId向微信发送Http请求获取二维码图片
        :return:
        """

        global WECHAT_SESSION_ID
        global WECHAT_TIMESPAN

        WECHAT_TIMESPAN = str(time.time())

        fetch_session_url = FETCH_SESSION_ID_URL.format(WECHAT_TIMESPAN)

        response = requests.get(fetch_session_url)

        WECHAT_SESSION_ID = response.text.replace(';', '').split('window.QRLogin.uuid =')[1].strip().replace('"', '')

        self.render('Home/login.html', session_id=WECHAT_SESSION_ID, timespan=WECHAT_TIMESPAN)

    def post(self, *args, **kwargs):
        """
        前端发送Ajax请求，检查用户是否已经使用手机扫码

        :param args:
        :param kwargs:
        :return:
        """
        ret_code = "201"

        code_url = CHECK_LOGIN_URL.format(WECHAT_SESSION_ID, WECHAT_TIMESPAN)
        # 请求URL，检查用户是否已经扫描二维码并登陆成功
        http_res_code = requests.get(code_url)

        if "window.code=201" in http_res_code.text:
            ret_code = "201"

        if "window.code=200" in http_res_code.text:
            # 用户已经通过手机扫过二维码，并成功

            code_cookie = http_res_code.cookies.get_dict()
            CODE_COOKIE_DICT.update(code_cookie)

            # 扫码成功后，获取下一步要请求的地址
            redirect_url = http_res_code.text.replace(';', '').replace('"', '').split('window.redirect_uri=')[1].strip()
            redirect_url += REDIRECT_URL_SUFFIX

            # 向得到的跳转地址发送Http请求，获取用户票据相关信息
            http_res_ticket = requests.get(redirect_url)

            ticket_cookies = http_res_ticket.cookies.get_dict()
            TICKET_COOKIE_DICT.update(ticket_cookies)

            ticket_result = self.auth_analysis(http_res_ticket)
            TICKET_RESULT_DICT.update(ticket_result)

            init_args = {
                "BaseRequest": {
                    "DeviceID": "e531777446530354",
                    "Sid": ticket_result['sid'],
                    "Skey": ticket_result['skey'],
                    "Uin": ticket_result['uin'],
                }
            }
            BASE_REQUEST_DICT.update(init_args)

            # 登陆之后，账号初始化
            init_cookies = {}
            init_cookies.update(code_cookie)
            init_cookies.update(ticket_cookies)
            ALL_COOKIE_DICT.update(init_cookies)

            init_url = USER_INIT_URL % (TICKET_RESULT_DICT['pass_ticket'], TICKET_RESULT_DICT['skey'], int(time.time()))
            origin = urllib2_request(init_url, init_args)
            INIT_RESULT_DICT.update(json.loads(origin))
            ret_code = "200"

        self.write(ret_code)

    def auth_analysis(self, http_res_ticket):
        message = re.search("(\<message\>)(.*)(\</message\>)",http_res_ticket.text).groups()[1]
        skey = re.search("(\<skey\>)(.*)(\</skey\>)",http_res_ticket.text).groups()[1]
        sid = re.search("(\<wxsid\>)(.*)(\</wxsid\>)",http_res_ticket.text).groups()[1]
        uin = re.search("(\<wxuin\>)(.*)(\</wxuin\>)",http_res_ticket.text).groups()[1]
        pass_ticket = re.search("(\<pass_ticket\>)(.*)(\</pass_ticket\>)",http_res_ticket.text).groups()[1]
        isgrayscale = re.search("(\<isgrayscale\>)(.*)(\</isgrayscale\>)",http_res_ticket.text).groups()[1]

        ret = {
            "message": message,
            "skey": skey,
            "sid": sid,
            "uin": uin,
            "pass_ticket": pass_ticket,
            "isgrayscale": isgrayscale,
        }

        return ret


class IndexHandler(tornado.web.RequestHandler):

    def get(self):
        try:
            print 'index'

            count = INIT_RESULT_DICT['Count']
            sync_key = INIT_RESULT_DICT['SyncKey']
            system_time = INIT_RESULT_DICT['SystemTime']
            skey = INIT_RESULT_DICT['SKey']

            client_version = INIT_RESULT_DICT['ClientVersion']
            base_response = INIT_RESULT_DICT['BaseResponse']
            MPSubscribeMsgCount = INIT_RESULT_DICT['MPSubscribeMsgCount']
            GrayScale = INIT_RESULT_DICT['GrayScale']
            InviteStartCount = INIT_RESULT_DICT['InviteStartCount']

            MPSubscribeMsgList = INIT_RESULT_DICT['MPSubscribeMsgList']

            ClickReportInterval = INIT_RESULT_DICT['ClickReportInterval']

            user = INIT_RESULT_DICT['User']
            CURRENT_USER.update(user)

            contact_list = INIT_RESULT_DICT['ContactList']

            self.render('Home/index.html', user=user, contact_list=contact_list, MPSubscribeMsgList=MPSubscribeMsgList)
        except Exception as e:
            self.redirect('/login')


class ContactList(tornado.web.RequestHandler):

    def get(self, *args, **kwargs):
        """
        获取所有用户信息
        :param args:
        :param kwargs:
        :return:
        """
        try:

            user_list_url = "https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxgetcontact?r=1377482079876"
            r1 = requests.post(user_list_url, data={}, cookies=ALL_COOKIE_DICT, headers={'contentType':'application/json;charset=UTF-8','Referer':'https://wx.qq.com/?&lang=zh_CN'})
            r1.encoding = 'utf-8'
            USER_LIST_DICT.update(json.loads(r1.text))
            self.render('Home/contact_list.html', user_list_dict=USER_LIST_DICT, user=CURRENT_USER)
        except Exception:
            self.redirect('/login')


class Message(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        global INIT_RESULT_DICT

        sync_url = "https://webpush.weixin.qq.com/cgi-bin/mmwebwx-bin/synccheck"

        sync_data_list = []
        for item in INIT_RESULT_DICT['SyncKey']['List']:
            temp = "%s_%s" % (item['Key'], item['Val'])
            sync_data_list.append(temp)
        sync_data_str = "|".join(sync_data_list)
        nid = int(time.time())
        sync_dict = {
            "r": nid,
            "skey": TICKET_RESULT_DICT['skey'],
            "sid": TICKET_RESULT_DICT['sid'],
            "uin": TICKET_RESULT_DICT['uin'],
            "deviceid": "e531777446530354",
            "synckey": sync_data_str
        }

        res_sync = requests.get(sync_url, params=sync_dict, cookies=ALL_COOKIE_DICT)
        print res_sync.text
        # if 'selector:"6"' in res_sync.text or 'selector:"7"' in res_sync.text:
        # 获取消息
        fetch_msg_url = "https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxsync?sid=%s&skey=%s&lang=zh_CN&pass_ticket=%s" % (TICKET_RESULT_DICT['sid'], TICKET_RESULT_DICT['skey'], TICKET_RESULT_DICT['pass_ticket'])
        fetch_msg_data = copy.deepcopy(BASE_REQUEST_DICT)
        fetch_msg_data['SyncKey'] = INIT_RESULT_DICT['SyncKey']
        fetch_msg_data['rr'] = nid

        res_fetch_msg = urllib2_request(fetch_msg_url, fetch_msg_data)
        res_fetch_msg_dict = json.loads(res_fetch_msg)

        INIT_RESULT_DICT['SyncKey'] = res_fetch_msg_dict['SyncKey']
        for item in res_fetch_msg_dict['AddMsgList']:
            print item['FromUserName'],"---->",item['ToUserName'], ":::::",item['Content']
        self.write("ok")


    def post(self, *args, **kwargs):
        message = self.get_argument('message')
        to_username = self.get_argument('username')

        init_data = copy.deepcopy(BASE_REQUEST_DICT)
        nid = str(time.time())
        init_data['Msg'] = {
                "ClientMsgId": nid,
                "Content": message,
                "FromUserName": CURRENT_USER['UserName'],
                "LocalID": nid,
                "ToUserName": to_username,
                "Type": 1
        }
        init_data['rr'] = nid

        send_url = "https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxsendmsg?lang=zh_CN&pass_ticket=" + TICKET_RESULT_DICT['pass_ticket']
        request = urllib2.Request(url=send_url, data=json.dumps(init_data))
        request.add_header('ContentType', 'application/json; charset=UTF-8')
        response = urllib2.urlopen(request)
        data = response.read()

        self.write(data)