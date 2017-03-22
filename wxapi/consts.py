from enum import Enum


class MaterialType(Enum):
    news = 'news'
    video = 'video'
    voice = 'voice'
    image = 'image'


class MsgType(Enum):
    text = 'text'
    image = 'image'
    voice = 'voice'
    video = 'video'
    music = 'music'
    news = 'news'
