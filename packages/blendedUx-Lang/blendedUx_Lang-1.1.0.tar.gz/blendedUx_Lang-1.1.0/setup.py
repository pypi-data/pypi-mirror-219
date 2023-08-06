#!/usr/bin/env python
import os
from setuptools import setup

DESCRIPTION = 'BlendedUx_lang'

setup(
    name='blendedUx_Lang',
    version="1.1.0",
    url='http://blended.dbmonline.net/',
    author='DBM',
    author_email='hbhadu@cognam.com',
    description=('Blended Command Line Application'),
    license='BSD',
    packages=['blended'],
    include_package_data=True,
    install_requires=[
        'markupsafe==2.1.2',
        'jinja2==3.1.2',
        'django==4.1.7'],
    zip_safe = False,
)

