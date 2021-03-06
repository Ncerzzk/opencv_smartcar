import tornado.ioloop
import tornado.web

from opencv_hcm import *
import numpy as np

import os
import time

class SaveHandle(tornado.web.RequestHandler):
    def get(self):
        for i in range(0,25):
            ret, image = self.application.cap.read()
        ret, image = self.application.cap.read()
        if ret:
            self.set_header("Content-Type", "image/jpeg")
            self.set_header("Refresh", "1")
            self.set_header("content-transfer-encoding", "binary")
            src=image.copy()
            image=get_cross2(image,True)
            image=None
            if image is None:
                image=src
            r, i = cv2.imencode('.jpg', image)
            if r:
                self.write(bytes(i.data))
            else:
                self.write('Sorry, encode faily!')
            name=str(int(time.time()))+".jpg"
            print(name)
            cv2.imwrite(name,image)


class CrossHandle(tornado.web.RequestHandler):
    def get(self):
        for i in range(0,25):
            ret, image = self.application.cap.read()
        ret, image = self.application.cap.read()
        if ret:
            self.set_header("Content-Type", "image/jpeg")
            self.set_header("Refresh", "1")
            self.set_header("content-transfer-encoding", "binary")
            src=image.copy()
            image=get_cross5(image,True)
            if image is None:
                image=src
            r, i = cv2.imencode('.jpg', image)
            if r:
                self.write(bytes(i.data))
            else:
                self.write('Sorry, encode faily!')
        else:
            self.write('Sorry, get camera data faily!')




class Application(tornado.web.Application):
    def __init__(self):
        handlers = [('/cross', CrossHandle),
                    ('/save',SaveHandle),
                    ]
        self.cap = cv2.VideoCapture(0)
        tornado.web.Application.__init__(self, handlers)

    def __del__(self):
        self.cap.release()

application = Application()

application.listen(8080)
tornado.ioloop.IOLoop.instance().start()
