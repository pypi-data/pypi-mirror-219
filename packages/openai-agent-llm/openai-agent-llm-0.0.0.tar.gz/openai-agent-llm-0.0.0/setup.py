#!/usr/bin/env python
# _*_ coding:utf-8 _*_

"""
File:   LogTool.py
Author: Lijiacai (1050518702@qq.com)
Date: 2018-11-20
Description:
   setup tool
"""

import os
import sys

from setuptools import setup
from setuptools import find_packages

setup(
    name="openai-agent-llm",  # 这里是pip 项目名称
    version="0.0.0",  # 发布的版本号，如果更新改库，那么会优先下载数值大的
    keywords=["openai-agent-llm", "openai", "agent"],  # 搜索关键字
    description="自定义LLM接口,使其兼容openai接口",
    long_description="自定义LLM接口,使其兼容openai接口",
    license="MIT License",
    url="",  # 这个是pip上的homepage,就是你源码的位置
    author="Lijiacai",  # 作者
    author_email="1050518702@qq.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=["loguru", "fastapi"]  # 这个项目需要的第三方库
)
