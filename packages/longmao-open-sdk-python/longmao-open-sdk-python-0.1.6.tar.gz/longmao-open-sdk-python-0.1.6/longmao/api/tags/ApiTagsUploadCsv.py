# coding=utf-8
#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2022-09-04
@author: nayuan
'''

from longmao.api.Api import Api
from longmao.core.exception.Exception import RequestException


class ApiTagsUploadCsv(Api):

    def __init__(self):
        super(ApiTagsUploadCsv, self).__init__('longmao.tags.upload', '20220904')

        self._title = None
        self._url = None

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self._url = value

    def get_params(self):

        if not self._title or not self._title.strip():
            raise RequestException("CSV描述[title]不能为空")
        if not self._url or not self._url.strip():
            raise RequestException("CSV链接[url]不能为空")

        data = dict()
        data['title'] = self._title
        data['url'] = self._url
        return data
