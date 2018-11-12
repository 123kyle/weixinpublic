#!/usr/bin/env python
# -*-coding:utf-8-*-
import requests
import settings
import json
import logging
logger = logging.getLogger("weixin")

class WeixinClient(object):

    def __init__(self, APPID, appsecrect):
        self.httpclient = requests.session()
        self.AppID = APPID
        self.AppSecret = appsecrect
        self.expires_in = 7200
        self.AccessToken = None
        self.getAccessToken()

    def init(self):
        ass_token = self.getAccessToken()
        self.AccessToken = ass_token

    def getAccessToken(self):
        res = self.httpclient.get(settings.WEIXINACCESSTOKENURL.format(
            self.AppID, self.AppSecret
        ))
        access_res = json.loads(res.content)
        if access_res.get('errcode'):
            logger.info('fetch AccessToken')
            return None
        else:
            self.AccessToken = access_res.get("access_token")

    def postImageMedia(self, file):
        url = settings.WEIXINMEDIAURL.format(self.AccessToken,
                                       "image")
        files = {"media": open(file,'rb')}
        res = self.httpclient.post(url, files=files,)
        return json.loads(res.content)

wexinClient = WeixinClient(settings.WEIXINAPPID,
                           settings.WEIXINAPPSECRECT)

