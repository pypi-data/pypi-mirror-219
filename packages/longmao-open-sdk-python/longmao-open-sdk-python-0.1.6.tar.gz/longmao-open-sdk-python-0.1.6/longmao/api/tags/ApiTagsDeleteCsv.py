# coding=utf-8
#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2022-09-04
@author: nayuan
'''

from longmao.api.Api import Api
from longmao.core.exception.Exception import RequestException

class ApiTagsDeleteCsv(Api):

    def __init__(self):
        super(ApiTagsDeleteCsv, self).__init__('longmao.tags.delete', '20230713')

        self._taskId = None

    @property
    def taskId(self):
        return self._taskId

    @taskId.setter
    def taskId(self, value):
        self._taskId = value

    def get_params(self):

        if not self._taskId or not self._taskId.strip():
            raise RequestException("[task_id]不能为空")

        data = dict()
        data['task_id'] = self._taskId
        return data
