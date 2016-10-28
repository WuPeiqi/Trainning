#!/usr/bin/env python
# -*- coding:utf-8 -*-


import Mapper
import tornado.ioloop
import tornado.web

settings = {
    'template_path': 'Views',
    'static_path': 'Statics',
    'static_url_prefix': '/statics/',
}

application = tornado.web.Application([
    #(r"/index", home.IndexHandler),
], **settings)


if __name__ == "__main__":
    Mapper.static_mapper()
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

