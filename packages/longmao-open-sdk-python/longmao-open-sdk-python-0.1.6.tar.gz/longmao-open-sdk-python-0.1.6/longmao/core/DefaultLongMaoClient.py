# coding=utf-8
#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2020-01-01
@author: nayuan
'''

import json
import requests
import platform

"""
龙猫数据开放平台接入客户端
"""
class DefaultLongMaoClient(object):

    """
    logger：日志对象，客户端执行信息会通过此日志对象输出
    """
    def __init__(self, config, logger=None):
        self._config = config
        self._logger = logger

    """
    执行接口请求
    """
    def execute(self, api):
        headers = {
            "Cache-Control": "no-cache",
            "Connection": "Keep-Alive",
            "User-Agent": "longmao-open-sdk-python/0.1.6 " + platform.platform() + ' ' + platform.python_version()
        }
        url = self._config.server_url + '?' + api.get_url_params(self._config)

        file = api.get_file()
        if not file:
            headers['Content-type'] = 'application/json;charset=' + self._config.charset
            result = requests.post(url, headers=headers, data=json.dumps(api.get_params()))
        else:
            result = requests.post(url, headers=headers, data=api.get_params(), files=file)

        return result.json()

