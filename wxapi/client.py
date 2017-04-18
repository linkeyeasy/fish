# encoding: utf-8

import logging
import json as jsonify
from os import path
from urlparse import urljoin
from hashlib import md5

from requests import get, post
from requests.exceptions import HTTPError

from .cached import cache
from .consts import MaterialType, MsgType
from .errors import HttpError, BusinessError
from .wrapper import Custom, IP, User, Token, OpenID, Material, MaterialCount, response

__version__ = '0.1.0'


class Client(object):
    """微信client"""

    logger = logging.getLogger(__name__)
    version = __version__

    cache_token = 'Client.get_token'

    def __init__(self, proto, host, app_id, app_secret, grant_type=None, access_token=None):
        self.proto = proto
        self.host = host
        self.base_url = '{schema}://{host}'.format(
            schema=self.proto, host=self.host)
        self.app_id = app_id
        self.app_secret = app_secret
        self._access_token = access_token
        self.grant_type = grant_type or 'client_credential'

    @property
    def access_token(self):
        self._access_token = self._access_token or self.get_token()
        return self._access_token

    def generate_uuid(self, filepath):
        m = md5()
        m.update(filepath)
        return m.hexdigest()

    def get(self, uri, params=None, **kwargs):
        url = urljoin(self.base_url, uri)
        r = get(url, params, **kwargs)
        try:
            if r.ok:
                json = r.json()
                if 'errcode' in json:
                    raise BusinessError(json)
                return json
        except HTTPError as e:
            raise HttpError(e)

    def post(self, uri, data=None, json=None, **kwargs):
        url = urljoin(self.base_url, uri)
        payload = jsonify.dumps(data, ensure_ascii=False)
        if not isinstance(payload, bytes):
            payload = payload.encode('utf-8')
        r = post(url, payload, json, **kwargs)
        try:
            if r.ok:
                json = r.json()
                code = json.get('errcode')
                if code and code < 1:
                    raise BusinessError(json)
                return json
        except HTTPError as e:
            raise HttpError(e)

    @response(Token)
    @cache(cache_token, time=7200)
    def get_token(self, grant_type=None):
        uri = '/cgi-bin/token'
        grant_type = grant_type or self.grant_type
        params = dict(grant_type=grant_type, appid=self.app_id,
                      secret=self.app_secret)
        return self.get(uri, params=params)

    @response(IP)
    def get_ips(self):
        uri = '/cgi-bin/getcallbackip'
        params = dict(access_token=self.access_token.access_token)
        return self.get(uri, params=params)

    @response(OpenID)
    def get_users(self, next_openid=None):
        """获取关注者列表"""
        uri = '/cgi-bin/user/get'
        params = dict(access_token=self.access_token.access_token,
                      next_openid=next_openid or '')

        return self.get(uri, params=params)

    @response(User)
    def get_user_info(self, openid, lang='zh_CN'):
        """获取关注者信息
            :parameter openid: 关注者的openid
            :parameter lang: 返回国家地区语言版本，zh_CN 简体，zh_TW 繁体，en 英语
        """
        uri = '/cgi-bin/user/info'
        params = dict(access_token=self.access_token.access_token,
                      openid=openid, lang=lang)

        return self.get(uri, params=params)

    @response(User)
    def get_users_batch(self):
        """
            批量获取用户基本信息
        """
        uri = '/cgi-bin/user/info/batchget'
        params = dict(access_token=self.access_token.access_token)

        return self.post(uri, data=params)

    @response(Material)
    def get_materials(self, material_type=MaterialType.news, offset=0, count=20):
        """
            获取素材列表
            return: {u'item': [], u'total_count': 0, u'item_count': 0}
        """
        uri = '/cgi-bin/material/batchget_material?access_token={}'.format(
            self.access_token.access_token)
        params = dict(type=material_type.value, offset=offset, count=count)
        return self.post(uri, data=params)

    @response(MaterialCount)
    def get_materials_count(self):
        """
            获取素材数量
        """
        uri = '/cgi-bin/material/get_materialcount?access_token={}'.format(
            self.access_token.access_token)

        return self.get(uri)

    @response(MaterialCount)
    def upload_materials(self, filepath, material_type=MaterialType.image):
        """
            上传素材
            1、对于临时素材，每个素材（media_id）会在开发者上传或粉丝发送到微信服务器3天后自动删除（所以用户发送给开发者的素材，若开发者需要，应尽快下载到本地），以节省服务器资源。
            2、media_id是可复用的。
            3、素材的格式大小等要求与公众平台官网一致。具体是，图片大小不超过2M，支持bmp/png/jpeg/jpg/gif格式，语音大小不超过5M，长度不超过60秒，支持mp3/wma/wav/amr格式
            4、需使用https调用本接口。
        """
        uri = '/cgi-bin/media/upload?access_token={}&type={}'.format(
            self.access_token.access_token, material_type.value)
        # 检查文件存在
        if not path.exists(filepath):
            return
        # 文件大小限制
        file_size = path.getsize(filepath)
        if file_size > 5 * 1024 * 1024:
            return

        file_ext = path.splitext(filepath)[1]
        filename = '{}{}'.format(self.generate_uuid(filepath), file_ext)
        files = {'file': (filename, open(filepath, 'rb'),
                          'application/oct-stream', {'Expires': '0'})}
        return self.post(uri, files=files)

    @response(Custom)
    def send_msg(self, content, openid, msg_type=MsgType.text):
        uri = '/cgi-bin/message/custom/send?access_token={}'.format(self.access_token.access_token)
        params = dict(msgtype=msg_type.value, touser=openid)
        if msg_type is MsgType.text:
            params[msg_type.value] = dict(content=content)
        return self.post(uri, data=params)
