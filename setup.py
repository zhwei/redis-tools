#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name='redis2s',
    version='dev',
    packages=['redis2s'],
    url='https://github.com/zhwei/redis-tools',
    install_requires=[
        'redis',
    ],
    license='MIT',
    author='zhwei',
    author_email='zhwei.yes@gmail.com',
    description='Python Common Redis Tools. '
)
