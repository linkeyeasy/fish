# encoding: utf-8

from sqlalchemy import func

from ext import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    openid = db.Column(db.String(32), unique=True)
    nickname = db.Column(db.String(32), default='-')

    # 用户的性别，值为1时是男性，值为2时是女性，值为0时是未知
    sex = db.Column(db.String(1), default=0)
    city = db.Column(db.String(32), default='-')
    country = db.Column(db.String(32), default='-')
    province = db.Column(db.String(32), default='-')
    language = db.Column(db.String(8), default='-')
    # 用户头像，最后一个数值代表正方形头像大小（有0、46、64、96、132数值可选，0代表640*640正方形头像），
    # 用户没有头像时该项为空。若用户更换头像，原有头像URL将失效。
    head_img_url = db.Column(db.String(1024), default='-')
    subscribe = db.Column(db.String(1), default=0)
    # 用户关注时间，为时间戳。如果用户曾多次关注，则取最后关注时间
    subscribe_time = db.Column(db.TIMESTAMP)
    union_id = db.Column(db.String(32), default=None)
    # 公众号运营者对粉丝的备注，公众号运营者可在微信公众平台用户管理界面对粉丝添加备注
    remark = db.Column(db.String(32), default=None)
    group_id = db.Column(db.String(32), default=None)
    tagid_list = db.Column(db.PickleType)
    update_time = db.Column(db.DateTime, nullable=False, server_default=func.now(),
                            server_onupdate=func.now(), doc='更新时间')
    creation_time = db.Column(db.DateTime, nullable=False, server_default=func.now(), doc='创建时间')

    def __repr__(self):
        return '<User %r> %r(%s)' % (self.openid, self.nickname, self.remark)

    @classmethod
    def get(cls, id_):
        return cls.query.get(id_)

    @classmethod
    def get_by_openid(cls, open_id):
        if open_id:
            return cls.query.filter_by(openid=open_id).first()

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def add_or_get(cls, **kwargs):
        openid = kwargs.get('openid')
        return cls.get_by_openid(openid) or cls.add(**kwargs)

    @classmethod
    def add(cls, openid, nickname, sex, city, country, province, language, headimgurl,
            subscribe, subscribe_time, unionid, remark, groupid, tagid_list):
        """
        {u'province': u'\u5317\u4eac',
        u'city': u'\u671d\u9633',
        u'subscribe_time': 1467039805,
        u'headimgurl': u'http://wx.qlogo.cn/mmopen/3Lqm1xHojtZbjhDFcS',
        u'language': u'zh_CN', u'country': u'\u4e2d\u56fd',
        u'tagid_list': [], u'remark': u'', u'sex': 1,
        u'subscribe': 1, u'unionid': u'o2R60wnDWZceOBmcyAjp1tqEqLSE',
        u'nickname': u'\u51af\u5f3a', u'groupid': 0}
        :param openid:
        :param nickname:
        :param sex:
        :param city:
        :param country:
        :param province:
        :param language:
        :param headimgurl:
        :param subscribe:
        :param subscribe_time:
        :param unionid:
        :param remark:
        :param groupid:
        :param tagid_list:
        :return:
        """
        instance = cls(openid=openid, nickname=nickname, sex=sex, city=city, country=country,
                       province=province, language=language, head_img_url=headimgurl,
                       subscribe=subscribe, subscribe_time=subscribe_time, union_id=unionid,
                       remark=remark, group_id=groupid, tagid_list=tagid_list)

        db.session.add(instance)
        db.session.commit()
        return instance

    @classmethod
    def update(cls, openid, nickname, sex, city, country, province, language, headimgurl,
               subscribe, subscribe_time, unionid, remark, groupid, tagid_list):
        instance = cls.query.filter_by(
            openid=openid).update(dict(nickname=nickname,
                                       sex=sex, city=city,
                                       country=country,
                                       province=province,
                                       language=language,
                                       head_img_url=headimgurl,
                                       subscribe=subscribe,
                                       subscribe_time=subscribe_time,
                                       union_id=unionid,
                                       remark=remark, group_id=groupid,
                                       tagid_list=tagid_list))
        db.session.commit()
        return instance
