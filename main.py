import tornado.ioloop
import tornado.web

import os

class CrossHandle(tornado.web.RequestHandler):
    def get(self):
        pass

application = tornado.web.Application([
        (r"/",IndexHandle),
],
login_url= 'login'
)
