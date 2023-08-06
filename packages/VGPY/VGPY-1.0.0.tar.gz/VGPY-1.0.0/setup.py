#!/usr/bin/env python
#-*- coding:utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='VGPY',
    version='1.0.0',
    description='van_go open api',
    author='JanVee',
    author_email='814107539@qq.com',
    packages=find_packages(),
    install_requires=[],
    keywords = ("vango", "VGPY"),
    long_description = "An feature extraction algorithm, van_go open api",
    license = "MIT Licence",
    url = "https://github.com/JanVee/VGPY",
    include_package_data = True,
    platforms = "any",
)