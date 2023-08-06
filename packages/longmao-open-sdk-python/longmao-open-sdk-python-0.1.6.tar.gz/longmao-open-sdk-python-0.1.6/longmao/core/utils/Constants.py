# coding=utf-8
#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2020-01-01
@author: nayuan
'''

import threading
import sys

PYTHON_VERSION_3 = True
if sys.version_info < (3, 0):
    PYTHON_VERSION_3 = False

THREAD_LOCAL = threading.local()