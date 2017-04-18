# encoding: utf-8


def response(cls):
    def wrapper(func):
        def wrapped(*args, **kwargs):
            return cls(func(*args, **kwargs))
        return wrapped
    return wrapper


class Entity(dict):

    def __init__(self, seq=None, **kwargs):
        for k, v in seq.items():
            self.__setattr__(k, v)
        super(Entity, self).__init__(seq, **kwargs)


class Custom(Entity):
    """
    通用结构
    """


class Token(Entity):
    """
        access_token : access_token_string
        expires_in : 7200
    """


class IP(Entity):
    """
    {
        "ip_list": [
            "127.0.0.1",
            "127.0.0.2",
            "101.226.103.0/25"
        ]
    }
    """


class OpenID(Entity):
    """
    {
   "total":23000,
   "count":3000,
   "data":{"
       "openid":[
         "OPENID20001",
         "OPENID20002",
         ...,
         "OPENID23000"
       ]
   },
   "next_openid":"OPENID23000"
    }
    """


class User(Entity):
    """用户信息
    {u'province': u'',
    u'city': u'',
    u'subscribe_time': 1483282466,
    u'headimgurl': u'http://wx.qlogo.cn/mmopen/3Lqm1xHojtay2V9laFYgaoKQUjO1m5ZDZiatlnZ90Y5j3Mqib1RObUdJvYibGGUTgtPQ3xOEPcysIbTibaibQeh8MaKFPlVSy4aGL/0',
    u'language': u'zh_CN', u'openid': u'orrRbwFYqkJcVvKaqCXW9WXOKQEw', u'country': u'\u4e2d\u56fd',
    u'tagid_list': [], u'remark': u'', u'sex': 2, u'subscribe': 1,
    u'unionid': u'o2R60wihCK4IjXSRSAIJCXLMD_nc', u'nickname': u'\u6e05\u6e05', u'groupid': 0}
    """


class Material(Entity):
    """素材

    """


class MaterialCount(Entity):
    """素材数量"""
