# coding=utf-8
#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2020-01-01
@author: nayuan
'''

class ApiException(Exception):
    def __init__(self):
        self.code = None
        self.message = None

    def __str__(self, *args, **kwargs):
        result = "code=" + self.code + \
             " message=" + self.message
        return result


class WrongModelTypeException(Exception):
    pass


class RequestException(Exception):
    pass


class ResponseException(Exception):
    pass