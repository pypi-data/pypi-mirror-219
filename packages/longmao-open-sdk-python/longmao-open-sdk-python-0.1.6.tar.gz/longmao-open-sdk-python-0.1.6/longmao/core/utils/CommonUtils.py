# coding=utf-8
#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2020-01-01
@author: nayuan
'''

try:
    from urllib.parse import quote_plus
except ImportError:
    from urllib import quote_plus

from longmao.core.utils.Constants import PYTHON_VERSION_3

def url_encode(params, charset):
    query_string = ""
    for (k, v) in params.items():
        value = v
        if PYTHON_VERSION_3:
            value = quote_plus(str(value), encoding=charset)
        else:
            value = quote_plus(str(value))
        query_string += ("&" + k + "=" + value)
    query_string = query_string[1:]
    return query_string

def has_value(m, key):
    if not m:
        return False
    if not (key in m):
        return False
    if not m[key]:
        return False
    return True


def get_file_suffix(bs):
    if not bs or len(bs) < 10:
      return None
    if PYTHON_VERSION_3:
        if bs[0] == 71 and bs[1] == 73 and bs[2] == 70:
            return "GIF"
        if bs[1] == 80 and bs[2] == 78 and bs[3] == 71:
            return "PNG"
        if bs[6] == 74 and bs[7] == 70 and bs[8] == 73 and bs[9] == 70:
            return "JPG"
        if bs[0] == 66 and bs[1] == 77:
            return "BMP"
    else:
        if ord(bs[0]) == 71 and ord(bs[1]) == 73 and ord(bs[2]) == 70:
          return "GIF"
        if ord(bs[1]) == 80 and ord(bs[2]) == 78 and ord(bs[3]) == 71:
          return "PNG"
        if ord(bs[6]) == 74 and ord(bs[7]) == 70 and ord(bs[8]) == 73 and ord(bs[9]) == 70:
          return "JPG"
        if ord(bs[0]) == 66 and ord(bs[1]) == 77:
          return "BMP"
    return None


def get_mime_type(bs):
    suffix = get_file_suffix(bs)
    mime_type = "application/octet-stream"
    if suffix == "JPG":
        mime_type = "image/jpeg"
    elif suffix == "GIF":
        mime_type = "image/gif"
    elif suffix == "PNG":
        mime_type = "image/png"
    elif suffix == "BMP":
        mime_type = "image/bmp"
    return mime_type

