#!/usr/bin/env python

from io import open
from setuptools import setup

"""

:authors: sergsadkov
:license: Apache License, Version 2.0, see LICENSE file
:copyright: (c) 2023 sergsadkov
"""


version = '0.0.1'

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='problem180meridian',
    version=version,

    author='sergsadkov',
    author_email='sergsadkov@gmail.com',

    description=(
        u'Python module to fix 180 degree crossing issue for vector geodata',
    ),

    long_description=long_description,
    long_description_content_type='text/markdown',

    url='https://github.com/sergsadkov/problem180meridian',
    download_url='https://github.com/sergsadkov/problem180meridian/archive/main.zip',

    license='Apache License, Version 2.0, see LICENSE file',

    packages=['problem180meridian'],
    install_requires=[],

    classifiers=[


        'Operating System :: OS Independent',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: CPython',
    ]
)