#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: Zhiyuan Wang
# Mail: 2073834696@qq.com
# Created Time:  2023-07-18
#############################################

from setuptools import setup, find_packages            #这个包没有的可以pip一下

setup(
    name = "tools_wzy",      #这里是pip项目发布的名称
    version = "0.0.2",  #版本号，数值大的会优先被pip
    keywords = ["pip", "tools_wzy"],
    description = "Some python tools for work from Zhiyuan",
    long_description = "Some python tools for work from Zhiyuan, improve the FastICA",
    license = "MIT Licence",

    url = "https://gitee.com/Zhiyuan_WZY",     #项目相关文件地址，一般是github
    author = "Zhiyuan Wang",
    author_email = "2073834696@qq.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ["pandas", "json", "datetime", "xml"]          #这个项目需要的第三方库
)

