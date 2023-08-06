#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from setuptools import setup, find_packages


with open("requirements.txt", encoding="utf-8") as r:
    requirements = [i.strip() for i in r]

with open("noelmode/__init__.py", "rt", encoding="utf8") as x:
    version = re.search(r'__version__ = "(.*?)"', x.read()).group(1)

with open('README.md') as f:
    long_description = f.read()


setup(
    name='noelmode',
    version=version,

    author='jokokendi',

    author_email='ajual7832@gmail.com',
    url='https://github.com/jokokendi/xmode',

    description='Pyromod Custom, Experimental Noel',
    long_description=long_description,
    long_description_content_type='text/markdown',

    download_url='https://github.com/jokokendi/xmode/archive/v{}.zip'.format(
        version
    ),
    license='GPLv3',

    packages=find_packages(),
    install_requires=requirements,
    python_requires="~=3.7",
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ]
)