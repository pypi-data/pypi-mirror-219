#!python
# -*- coding:utf-8 -*-
from __future__ import print_function
from setuptools import setup, find_packages
import longyuanpower

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name="longyuanpower",
    version=1.0,
    author="yuange_liu, daobin_luo",
    author_email="liuyuange811@gmail.com, luodaobin2001@gmail.com",
    description="A module for turbine power prediction",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/962516016/longyuanpower",
    py_modules=['longyuanpower'],
    install_requires=[
        "requests <= 2.31.0"
        ],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        'Programming Language :: Python :: Implementation :: CPython',
    ],
)

