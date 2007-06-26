##############################################################################
#
# Copyright (c) 2007 Zope Foundation and Contributors.
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
"""Setup

$Id$
"""
import os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup(
    name='grok',
    version='0.9',
    author='Grok Team',
    author_email='grok-dev@zope.org',
    url='https://launchpad.net/grok',
    download_url='svn://svn.zope.org/repos/main/grok/trunk#egg=grok-dev',
    description='Grok: Now even cavemen can use Zope 3!',
    long_description=open('README.txt').read(),
    license='ZPL',
    packages = find_packages('src'),
    include_package_data = True,
    package_dir = {'':'src'},
    dependency_links = ['http://download.zope.org/distribution'],
    zip_safe = False,
      install_requires=['setuptools',
                        'zope.annotation',
                        'zope.copypastemove',
                        'zope.contentprovider',
                        'zope.event',
                        'zope.formlib',
                        'zope.i18n',
                        'zope.publisher',
                        'zope.security',
                        'zope.size',
                        'zope.traversing',
                        'zope.testbrowser',
                        'zope.viewlet',
                        'zope.app.securitypolicy',
                        'zope.app.authentication',
                        'zope.app.catalog',
                        'zope.app.intid',
                        'zope.app.keyreference',
                        'zope.app.twisted',
                        'zope.app.session',
                        'zope.app.zcmlfiles',
                        'zope.app.file',
                        'simplejson',
                        # -*- Extra requirements: -*-
                        ],
      entry_points="""
      # -*- Entry points: -*-
      """,
    )
