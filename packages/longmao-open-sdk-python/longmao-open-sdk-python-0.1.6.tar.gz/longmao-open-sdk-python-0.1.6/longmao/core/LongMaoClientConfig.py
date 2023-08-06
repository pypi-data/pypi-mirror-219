# coding=utf-8
#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2020-01-01
@author: nayuan
'''


class LongMaoClientConfig(object):

    def __init__(self):

        # 开发者accessKeyId
        self._access_key_id = ''
        # 开发者accessKeySecret
        self._access_key_secret = ''

        # 龙猫数据开放平台网关地址
        self._server_url = "https://api.service.longmaosoft.com/gateway.do"
        # 请求字符集，默认utf-8
        self._charset = 'utf-8'
        # 请求响应报文格式
        self._format = 'JSON'
        # 请求读取超时，单位秒，默认15s
        self._timeout = 5

    @property
    def domain(self):
        return self._server_url

    @domain.setter
    def domain(self, value):
        self._server_url = value

    @property
    def access_key_id(self):
        return self._access_key_id

    @access_key_id.setter
    def access_key_id(self, value):
        self._access_key_id = value

    @property
    def access_key_secret(self):
        return self._access_key_secret

    @access_key_secret.setter
    def access_key_secret(self, value):
        self._access_key_secret = value

    @property
    def server_url(self):
        return self._server_url

    @server_url.setter
    def server_url(self, value):
        self._server_url = value

    @property
    def charset(self):
        return self._charset

    @charset.setter
    def charset(self, value):
        self._charset = value

    @property
    def format(self):
        return self._format

    @format.setter
    def format(self, value):
        self._format = value

    @property
    def timeout(self):
        return self._timeout

    @timeout.setter
    def timeout(self, value):
        self._timeout = value



