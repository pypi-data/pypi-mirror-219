# -*- coding: utf-8 -*-
# @Author  : jackxclei
# @Time    : 2023/7/17 11:39 上午
# @Function:
from setuptools import setup, find_packages

setup(
    name="medcase",
    version="0.1.8",
    packages=find_packages(),
    install_requires=[
        # 添加项目依赖
        # "tkcalendar",
        "datetime",
        "requests",
        "tkcalendar",
    ],
    entry_points={
        "console_scripts": [
            "medcase=medcase.autogui:main",
        ],
    },
)