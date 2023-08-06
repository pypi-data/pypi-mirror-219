# coding=utf-8
#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2020-01-01
@author: nayuan
'''

import time
from longmao.core.utils.SignatureUtils import sign_with_md5
from longmao.core.utils.CommonUtils import url_encode

class Api(object):

    def __init__(self, method, version):
        self._method = method
        self._version = version

    def get_url_params(self, config):
        url_params = dict()
        url_params['access_key_id'] = config.access_key_id
        url_params['method'] = self._method
        url_params['version'] = self._version
        url_params['format'] = config.format
        url_params['timestamp'] = int(round(time.time() * 1000))
        url_params['sign'] = sign_with_md5(url_params, config.access_key_secret, config.charset)

        query_string = url_encode(url_params, config.charset)
        return query_string

    def get_params(self):
        return None

    def get_file(self):
        return None