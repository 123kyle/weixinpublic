#!/usr/bin/env python
# -*-coding:utf-8-*-

MESSAGE_TYPES = {}

def register_message(msg_type):
    def wrapper(cls):
        MESSAGE_TYPES[msg_type] = cls
        return cls

    return wrapper


class Message(object):
    MsgId = None
    ToUserName = None
    FromUserName = None
    CreateTime = None
    MsgType = None

    def __str__(self):
        return "".join(["{name}:{value}\n".format(name=i,
                                                  value=getattr(self, i))
                        for i in dir(self) if i[0].isupper()])
@register_message('text')
class TextMessage(Message):
    Content = None


@register_message('image')
class ImageMessage(Message):
    PicUrl = None
    Mediald = None
