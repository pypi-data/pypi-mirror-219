# -*- coding: utf-8 -*-
#!/usr/bin/python
'''
 Licensed to the Apache Software Foundation (ASF) under one
 or more contributor license agreements.  See the NOTICE file
 distributed with this work for additional information
 regarding copyright ownership.  The ASF licenses this file
 to you under the Apache License, Version 2.0 (the
 "License"); you may not use this file except in compliance
 with the License.  You may obtain a copy of the License at
     http://www.apache.org/licenses/LICENSE-2.0
 Unless required by applicable law or agreed to in writing,
 software distributed under the License is distributed on an
 "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 KIND, either express or implied.  See the License for the
 specific language governing permissions and limitations
 under the License.
'''

import codecs
import os

from setuptools import setup, find_packages

"""
setup module for core.
Created on 2020-01-01
@author: nayuan
"""
PACKAGE = "longmao"
NAME = "longmao-open-sdk-python"
DESCRIPTION = "The official LongMao SDK for Python."
AUTHOR = "nayuan"
AUTHOR_EMAIL = "haojunsheng@longmaosoft.com"
URL = "https://github.com/nayuan/longmao-open-sdk-python"

TOPDIR = os.path.dirname(__file__) or "."
VERSION = __import__(PACKAGE).__version__

desc_file = codecs.open("README.rst", 'r', 'utf-8')
try:
    LONG_DESCRIPTION = desc_file.read()
finally:
    desc_file.close()

requires = ["requests"]

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license="Apache",
    url=URL,
    keywords=["longmao", 'open', "sdk"],
    packages=find_packages(exclude=["tests*"]),
    include_package_data=True,
    platforms='any',
    install_requires=requires,
    classifiers=(
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Topic :: Software Development',
    )
)
