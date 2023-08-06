# coding=utf-8
#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2020-01-01
@author: nayuan
'''

import hashlib

def sign_with_md5(urlParams, secret, charset):
    sign_content = ""
    for (k, v) in sorted(urlParams.items()):
        sign_content += ("&" + k + "=" + str(v))
    sign_content = sign_content[1:] + secret

    md5 = hashlib.md5()
    md5.update(sign_content.encode(charset))
    return md5.hexdigest().upper()