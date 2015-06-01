# -*- coding: utf-8 -*-

import sys
import os

import tornado.ioloop
import tornado.web
import tornado.options
import tornado.httpserver

from tornado.options import define, options

from mako.lookup import TemplateLookup
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from router import handlers
from config import Config, LISTENER_IP, COOKIE_SALT, DEBUG

reload(sys)
sys.setdefaultencoding('utf-8')

define("port", default=9501, help="run on the given port", type=int)

class Application(tornado.web.Application):

    def __init__(self):

        setting = dict(
            cookie_secret=COOKIE_SALT,
            autoreload=True,
            gzip=True,
            debug=DEBUG,
            login_url='/login/',
            static_path=os.path.join(os.path.dirname(__file__), "static"),
        )

        tornado.web.Application.__init__(self, handlers, **setting)

        # templates
        self.template_lookup = TemplateLookup(
                directories=[os.path.join(os.path.dirname(__file__), 'templates')],
                module_directory=os.path.join(os.path.dirname(__file__), 'tmp/mako_modules'),
                input_encoding='utf-8',
                output_encoding='utf-8',
                default_filters=['decode.utf8'],
                encoding_errors='replace',
                )
        # db
        engine = create_engine(
                Config['mysql-mysqldb'], encoding='utf-8', echo=False,
                pool_recycle=600, pool_size=20, max_overflow=100
                )
        self.DB_Session = sessionmaker(bind=engine)

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port, address=LISTENER_IP)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
