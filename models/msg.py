# encoding: utf-8

from sqlalchemy import func

from ext import db


class Msg(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    msg_id = db.Column(db.String(32), unique=True)
    msg_type = db.Column(db.String(32), default='-')

    # user openid
    from_user = db.Column(db.String(32), default=0)
    to_user = db.Column(db.String(32), default='-')
    event = db.Column(db.String(32), default='-')
    content = db.Column(db.Text, default='-')

    # pic media
    pic_url = db.Column(db.String(1024), default='-')
    media_id = db.Column(db.String(32), default='-')

    # voice
    fmt = db.Column(db.String(8), default='-')
    recognition = db.Column(db.Text, default='-')

    # video & music
    thumb_id = db.Column(db.String(64), default='-')

    # location
    x = db.Column(db.DECIMAL, default=0)
    y = db.Column(db.DECIMAL, default=0)
    scale = db.Column(db.Integer, default=0)
    label = db.Column(db.String(512), default='')

    update_time = db.Column(db.DateTime, nullable=False, server_default=func.now(),
                            server_onupdate=func.now(), doc='更新时间')
    creation_time = db.Column(db.DateTime, nullable=False, doc='创建时间')

    def __repr__(self):
        return '<Msg %r> %s(%s)' % (self.openid, self.nickname, self.remark)

    @classmethod
    def get(cls, id_):
        return cls.query.get(id_)

    @classmethod
    def get_by_msg_id(cls, msg_id):
        if msg_id:
            return cls.query.filter_by(openid=msg_id).first()

    @classmethod
    def get_all(cls):
        return cls.query.order_by(-cls.creation_time).limit(100).all()

    @classmethod
    def add_or_get(cls, **kwargs):
        msg_id = kwargs.get('msg_id')
        return cls.get_by_msg_id(msg_id) or cls.add(**kwargs)

    @classmethod
    def add(cls, msg_id, msg_type, from_user, to_user, content, event=None, pic_url=None,
            media_id=None, fmt=None, recognition=None, thumb_id=None, x=None, y=None, scale=None,
            label=None, creation_time=None):
        instance = cls(msg_id=msg_id, msg_type=msg_type, from_user=from_user, to_user=to_user,
                       event=event, content=content, pic_url=pic_url, media_id=media_id,
                       fmt=fmt, recognition=recognition, thumb_id=thumb_id,
                       x=x, y=y, scale=scale, label=label, creation_time=creation_time)

        db.session.add(instance)
        db.session.commit()
        return instance

    @classmethod
    def update(cls, msg_id, **kwargs):
        instance = cls.query.filter_by(openid=msg_id).update(kwargs)
        db.session.commit()
        return instance
