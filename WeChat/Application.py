#!/usr/bin/env python
# -*- coding:utf-8 -*-

import tornado.ioloop
import tornado.web

from Controllers import HomeController

settings = {
    'static_path': 'Statics',
    'static_url_prefix': '/static/',
    'template_path': 'Views',
}


application = tornado.web.Application([
    (r"/login", HomeController.LoginHandler),
    (r"/index", HomeController.IndexHandler),
    (r"/contact_list", HomeController.ContactList),
    (r"/msg", HomeController.Message),
], **settings)


if __name__ == "__main__":
    application.listen(8003)
    print 'running http://localhost:8003/login'
    tornado.ioloop.IOLoop.instance().start()