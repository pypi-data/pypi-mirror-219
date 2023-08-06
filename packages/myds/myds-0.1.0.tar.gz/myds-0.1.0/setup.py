#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: Cai Jianping
# Mail: jpingcai@163.com
# Created Time:  2022-7-9 11:25:34 AM
#############################################


from setuptools import setup, find_packages

setup(
    name = "myds",
    version = "0.1.0",
    keywords = ("database","localServer"),
    description = "A database name Getter",
    long_description = "A database name Getter",
    license = "MIT Licence",
    author = "Cai Jianping",
    author_email = "jpingcai@163.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ['requests','urllib3']
)
