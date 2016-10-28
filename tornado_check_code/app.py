#!/usr/bin/env python
# -*- coding:utf-8 -*-

import tornado.ioloop
import tornado.web
import io
import check_code



class CheckCodeHandler(tornado.web.RequestHandler):
    def get(self):

        mstream = io.BytesIO()
        img, code = check_code.create_validate_code()
        img.save(mstream, "GIF")
        self.write(mstream.getvalue())


class QrCodeHandler(tornado.web.RequestHandler):
    def get(self):
        import qrcode

        mstream = io.BytesIO()
        img = qrcode.make('http://www.baidu.com')
        img.save(mstream, "png")

        self.write(mstream.getvalue())

class MainHandler(tornado.web.RequestHandler):
    def get(self):

        self.render('index.html')

    def post(self, *args, **kwargs):
        print(123)
        self.write('post')

settings = {
    'template_path': 'template',
    'static_path': 'static',
    'static_url_prefix': '/static/',
    'cookie_secret': 'aiuasdhflashjdfoiuashdfiuh',
    'xsrf_cookies': True
}

application = tornado.web.Application([
    (r"/index", MainHandler),
    (r"/check_code", CheckCodeHandler),
    (r"/qr_code", QrCodeHandler),
], **settings)


if __name__ == "__main__":
    application.listen(8889)
    tornado.ioloop.IOLoop.instance().start()