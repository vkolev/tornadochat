#!/usr/bin/env python
# encoding: utf-8

import time
import logging
import signal
import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpserver
import os.path
import uuid

from tornado.options import define, options

from app.base import MainHandler
from app.chattr import ChatSocketHandler
from app.login import LoginHandler
from app.logout import LogoutHandler

define("port", default=8888, help="run on the given port", type=int)

MAX_WAIT_SECONDS_BEFORE_SHUTDOWN = 3

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
		(r"/", MainHandler),
		(r"/login", LoginHandler),
		(r"/logout", LogoutHandler),
		(r"/chatsocket", ChatSocketHandler),
		]
	settings = dict(
		cookie_secret="mzOwNs3KreTk3Y!",
		template_path=os.path.join(os.path.dirname(__file__), "templates"),
		static_path=os.path.join(os.path.dirname(__file__), "static"),
		xsrf_cookies=True,
		)
	tornado.web.Application.__init__(self, handlers, **settings)

def sig_handler(sig, frame):
    logging.warning('Caught signal: %s', sig)
    tornado.ioloop.IOLoop.instance().add_callback(shutdown)

def shutdown():
    logging.info('Stopping http server')
    server.stop()

    logging.info('Will shutdown in %s seconds ...', MAX_WAIT_SECONDS_BEFORE_SHUTDOWN)
    io_loop = tornado.ioloop.IOLoop.instance()

    deadline = time.time() + MAX_WAIT_SECONDS_BEFORE_SHUTDOWN

    def stop_loop():
	now = time.time()
	if now < deadline and (io_loop._callbacks or io_loop._timeouts):
	    io_loop.add_timeout(now + 1, stop_loop)
	else:
	    io_loop.stop()
	    logging.info('Shutdown')
	stop_loop()

def main():
    tornado.options.parse_command_line()
    application = Application()
    global server
    server = tornado.httpserver.HTTPServer(application)
    server.listen(options.port)

    tornado.ioloop.IOLoop.instance().start()

    logging.info("Exit...")

if __name__ == '__main__':
    main()
