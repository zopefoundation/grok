##############################################################################
#
# Copyright (c) 2007 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Setup for grokcore.grok package
"""
from setuptools import setup, find_packages

setup(
    name='grokcore.grok',
    version='0.1',
    author='Grok Team',
    author_email='grok-dev@zope.org',
    url='http://grok.zope.org',
    download_url='http://cheeseshop.python.org/pypi/grokcore.grok/',
    description='Facilities for grokking from Python and ZCML',
    long_description=open('README.txt').read(),
    license='ZPL',
    packages=find_packages(),
    namespace_packages=['grokcore'],
    include_package_data = True,
    zip_safe=False,
    install_requires=['setuptools',
                      'martian',
                      'zope.configuration',
                      ],
)
