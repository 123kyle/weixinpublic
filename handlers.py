#!/usr/bin/env python
# -*-coding:utf-8-*-

import string
import os
import random
import time
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse
from tornado.web import RequestHandler
from tornado.web import Application
from tornado.ioloop import IOLoop, PeriodicCallback
from tornado.gen import coroutine
from tornado.options import define, options
from template import TEXT_TEMPLATE, IMAGE_TEMPLATE
import xml.etree.ElementTree as ET
from message import MESSAGE_TYPES
from instagram import Instagram
from settings import BASEPATH, WEIXINEXPIRESTIME
from weixin import wexinClient


define("port", default=8888, help="run on the given port", type=int)

Executor = ThreadPoolExecutor(max_workers=4)

def parse(xmlstring):
    msgXML = ET.fromstring(xmlstring)
    msg_type = msgXML.find("MsgType").text
    if MESSAGE_TYPES.get(msg_type):
        clsObj = MESSAGE_TYPES.get(msg_type)()
        for item in msgXML:
            if hasattr(clsObj, item.tag):
                setattr(clsObj,item.tag, item.text)
        return clsObj

def parseurl(urlstring):
    urlObj = urlparse(urlstring)
    return "{}://{}{}".format(urlObj.scheme,urlObj.netloc,urlObj.path)

class MainHandler(RequestHandler):

    def get(self):
        signature = self.get_argument("signature")
        timestamp = self.get_argument("timestamp")
        nonce = self.get_argument("nonce")
        echostr = self.get_argument("echostr")
        self.write(echostr)

    @coroutine
    def post(self, *args, **kwargs):
        userSend = self.request.body.decode()
        msgobj = parse(userSend)
        if msgobj.MsgType == "text":
            if "instagram.com" in msgobj.Content:
                realurl = parseurl(msgobj.Content)
                insobj = Instagram(BASEPATH,realurl)
                imagePath = yield Executor.submit(insobj.fetchImage)
                res = yield Executor.submit(wexinClient.postImageMedia,
                                            imagePath)
                imgrepsone = IMAGE_TEMPLATE.format(
                    to_user=msgobj.FromUserName,
                    from_user=msgobj.ToUserName,
                    create_time=int(time.time()),
                    media_id=res.get("media_id"),
                )
                self.write(imgrepsone)
                return


        self.write("success")


def main():
    options.parse_command_line()
    printable = string.ascii_uppercase + string.digits
    rand = ''
    for _ in range(128):
        rand += random.SystemRandom().choice(printable)

    SETTINGS = {
        "static_path": os.path.join(BASEPATH, "static"),
        "static_url_prefix": "/static/",
        "template_path": os.path.join(BASEPATH, "templates"),
        "cookie_secret": rand,
        "login_url": "/login",
        "xsrf_cookies": False,
    }

    imgFolder = os.path.join(BASEPATH, "img")
    if not os.path.isdir(imgFolder):
        os.mkdir(imgFolder)
    app = Application(
        [(r"/weixin", MainHandler)], **SETTINGS
    )
    app.listen(options.port)
    PeriodicCallback(wexinClient.getAccessToken,1000 * WEIXINEXPIRESTIME).start()
    try:
        IOLoop.current().start()
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()



