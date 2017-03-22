from __future__ import absolute_import

from unittest import TestCase

from .client import Client
from .wrapper import Token, OpenID


class Test(TestCase):

    def setUp(self):
        self.client = Client('https', 'api.weixin.qq.com', 'wx16c9d45585b6c9dd',
                             '73bcfc9d8f304a4a5ac33467b921a55d')
        self.token = None

    def test_get_token(self):
        self.token = self.client.get_token()
        self.assertIsNotNone(self.token)
        self.assertIsInstance(self.token, Token)
        assert self.token.access_token is not None
        self.assertEqual(self.token.expires_in, 7200)

    def test_get_ip_list(self):
        ip_list = self.client.get_ips()
        self.assertTrue(isinstance(ip_list.ip_list, list))

    def test_get_openid(self):
        users = self.client.get_users()
        self.assertIsInstance(users, OpenID)

    def test_get_user_info(self):
        users = self.client.get_users()
        last_user = self.client.get_user_info(users.next_openid)
        self.assertIsNotNone(last_user)

    def test_get_materials(self):
        materials = self.client.get_materials()
        self.assertIsNotNone(materials)

    def test_get_materials_count(self):
        count = self.client.get_materials_count()
        self.assertIsNotNone(count)

    def tearDown(self):
        pass
