#!/usr/bin/env python
# -*-coding:utf-8-*-
import os


BASEPATH = os.path.dirname(os.path.abspath(__file__))

WEIXINACCESSTOKENURL = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}"

WEIXINAPPID = os.environ.get("WEIXINAPPID")

WEIXINAPPSECRECT = os.environ.get("WEIXINAPPSECRECT")

WEIXINEXPIRESTIME = 7200

WEIXINTOKEN = os.environ.get("WEIXINTOKEN")

WEIXINENCODINGAESKEY = os.environ.get("WEIXINENCODINGAESKEY")

# access_token 调用接口凭证
# type 图片（image）、语音（voice）、视频（video）和缩略图（thumb）
# media form-data中媒体文件标识，有filename、filelength、content-type等信息
WEIXINMEDIAURL = "https://api.weixin.qq.com/cgi-bin/media/upload?access_token={}&type={}"
