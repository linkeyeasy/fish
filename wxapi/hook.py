# encoding: utf-8

from operator import itemgetter

from flask import request

try:
    import xml.etree.cElementTree as ETree
except ImportError:
    import xml.etree.ElementTree as ETree


def incoming(*classes):
    """hook incoming messages"""

    if not all(issubclass(cls, Message) for cls in classes):
        raise RuntimeError('not a subclass of <{}>'.format(Message.__name__))

    def wrapper(func):
        def wrapped(*args, **kwargs):
            print '/////////////////////////////////////'
            print request.data
            print '-------------------------------------'
            tree = ETree.fromstring(request.data)
            msg = Message((element.tag, element.text) for element in tree)
            for cls in classes:
                if msg.msg_type == 'event':
                    if msg.event == cls.__name__.lower():
                        return func(cls(msg), *args, **kwargs)
                elif msg.msg_type == cls.__name__.lower():
                    return func(cls(msg), *args, **kwargs)
            return func(msg, *args, **kwargs)

        return wrapped

    return wrapper


class Message(dict):
    """
    基础消息类
    """
    msg_id = property(itemgetter('MsgId'))
    msg_type = property(itemgetter('MsgType'))
    to_user = property(itemgetter('ToUserName'))
    from_user = property(itemgetter('FromUserName'))
    create_time = property(itemgetter('CreateTime'))
    event = property(itemgetter('Event'))


class Text(Message):
    """
        <xml>
            <ToUserName><![CDATA[{to_user}]]></ToUserName>
            <FromUserName><![CDATA[{from_user}]]></FromUserName>
            <CreateTime>{create_time}</CreateTime>
            <MsgType><![CDATA[text]]></MsgType>
            <Content><![CDATA[{content}]]></Content>
        </xml>
    """
    content = property(itemgetter('Content'))


class Image(Message):
    """
        <xml><ToUserName><![CDATA[gh_6cafe8fadb1b]]></ToUserName>
        <FromUserName><![CDATA[orrRbwKLJYHeqjKFL1EN9Hp-bppo]]></FromUserName>
        <CreateTime>1483944468</CreateTime>
        <MsgType><![CDATA[image]]></MsgType>
        <PicUrl><![CDATA[http://mmbiz.qpic.cn/mmbiz_jpg/8vU1xNaQE5qSVsWhALMtdJs77mF33KaAVpWZibCQGIG8nGibQDFeMQ2RlSulhdWh0FL4T6y4VLNCQR7ITBtKlODg/0]]></PicUrl>
        <MsgId>6373492959558551518</MsgId>
        <MediaId><![CDATA[RI9ylOtAsJwsAcFeMhdjz3xNHd6ipuqKgcqp0xkVOE6J1BAbbLd2V_sRH1s6Mmv2]]></MediaId>
        </xml>
    """

    pic_url = property(itemgetter('PicUrl'))
    media_id = property(itemgetter('MediaId'))


class Voice(Message):
    """
        <xml>
        <ToUserName><![CDATA[gh_6cafe8fadb1b]]></ToUserName>
        <FromUserName><![CDATA[orrRbwKLJYHeqjKFL1EN9Hp-bppo]]></FromUserName>
        <CreateTime>1483943389</CreateTime>
        <MsgType><![CDATA[voice]]></MsgType>
        <MediaId><![CDATA[tmBEAGq-gfPfDbzZKLy003GU195was4pJ0ZYpnOWKWvXxki6Ee2Xne-KRqXuhB7K]]></MediaId>
        <Format><![CDATA[amr]]></Format>
        <MsgId>6373488324870406144</MsgId>
        <Recognition><![CDATA[哦。]]></Recognition>
        </xml>
    """

    fmt = property(itemgetter('Format'))
    media_id = property(itemgetter('MediaId'))
    recognition = property(itemgetter('Recognition'))


class Video(Message):
    """
        <xml>
        <ToUserName><![CDATA[gh_6cafe8fadb1b]]></ToUserName>
        <FromUserName><![CDATA[orrRbwKLJYHeqjKFL1EN9Hp-bppo]]></FromUserName>
        <CreateTime>1483943720</CreateTime>
        <MsgType><![CDATA[video]]></MsgType>
        <MediaId><![CDATA[N-RG6Cuu5CSMYeWU0DbI5Z7Wgc1ugZ8wk3ECSQCFY1VFQh-BNf5iA42_a6CJ4327]]></MediaId>
        <ThumbMediaId><![CDATA[KQ7QOnfaUBF7S6Mc9zzvVGrRJX5iyIs8mev9OmHZUP0UMR6uE7iyW0JiSCVgSc5r]]></ThumbMediaId>
        <MsgId>6373489746923013440</MsgId>
        </xml>
    """

    media_id = property(itemgetter('MediaId'))
    thumb_id = property(itemgetter('ThumbMediaId'))


class Music(Message):
    """
        <xml>
        <ToUserName><![CDATA[gh_6cafe8fadb1b]]></ToUserName>
        <FromUserName><![CDATA[orrRbwKLJYHeqjKFL1EN9Hp-bppo]]></FromUserName>
        <CreateTime>1483943720</CreateTime>
        <MsgType><![CDATA[video]]></MsgType>
        <MediaId><![CDATA[N-RG6Cuu5CSMYeWU0DbI5Z7Wgc1ugZ8wk3ECSQCFY1VFQh-BNf5iA42_a6CJ4327]]></MediaId>
        <ThumbMediaId><![CDATA[KQ7QOnfaUBF7S6Mc9zzvVGrRJX5iyIs8mev9OmHZUP0UMR6uE7iyW0JiSCVgSc5r]]></ThumbMediaId>
        <MsgId>6373489746923013440</MsgId>
        </xml>
    """

    media_id = property(itemgetter('MediaId'))
    thumb_id = property(itemgetter('ThumbMediaId'))


class Location(Message):
    """
        <xml><ToUserName><![CDATA[gh_6cafe8fadb1b]]></ToUserName>
        <FromUserName><![CDATA[orrRbwKLJYHeqjKFL1EN9Hp-bppo]]></FromUserName>
        <CreateTime>1483943965</CreateTime>
        <MsgType><![CDATA[location]]></MsgType>
        <Location_X>39.906490</Location_X>
        <Location_Y>116.474096</Location_Y>
        <Scale>15</Scale>
        <Label><![CDATA[北京市朝阳区现代城西路光辉南里(SOHO现代城旁)]]></Label>
        <MsgId>6373490799190001166</MsgId>
        </xml>
    """
    x = property(itemgetter('Location_X'))
    y = property(itemgetter('Location_Y'))
    scale = property(itemgetter('Scale'))
    label = property(itemgetter('Label'))


class View(Message):
    """
        <xml>
        <ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[FromUser]]></FromUserName>
        <CreateTime>123456789</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[VIEW]]></Event>
        <EventKey><![CDATA[www.qq.com]]></EventKey>
        </xml>
    """
    key = property(itemgetter('EventKey'))


class Qrscene(Message):
    """
        <xml><ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[FromUser]]></FromUserName>
        <CreateTime>123456789</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[subscribe]]></Event>
        <EventKey><![CDATA[qrscene_123123]]></EventKey>
        <Ticket><![CDATA[TICKET]]></Ticket>
        </xml>
    """
    key = property(itemgetter('EventKey'))
    ticket = property(itemgetter('Ticket'))
