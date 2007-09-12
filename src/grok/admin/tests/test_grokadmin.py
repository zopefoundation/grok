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
"""Setup for tests."""

import os
import unittest
from pkg_resources import resource_listdir
from zope.testing import doctest, cleanup
import zope.component.eventtesting
from zope.annotation.attribute import AttributeAnnotations

def setUpZope(test):
    zope.component.eventtesting.setUp(test)
    zope.component.provideAdapter(AttributeAnnotations)

def cleanUpZope(test):
    cleanup.cleanUp()

def suiteFromPackage(name):
    files = resource_listdir(__name__, name)
    suite = unittest.TestSuite()
    for filename in files:
        if not filename.endswith('.py'):
            continue
        if filename.endswith('_fixture.py'):
            continue
        if filename == '__init__.py':
            continue

        dottedname = 'grok.admin.tests.%s.%s' % (name, filename[:-3])
        test = doctest.DocTestSuite(dottedname,
                                    setUp=setUpZope,
                                    tearDown=cleanUpZope,
                                    optionflags=doctest.ELLIPSIS+
                                    doctest.NORMALIZE_WHITESPACE)

        suite.addTest(test)
    return suite

def pnorm(path):
    """Normalization of paths to use forward slashes. This is needed
    to make sure the tests work on windows.
    """
    return path.replace(os.sep, '/')

def test_suite():
    suite = unittest.TestSuite()
    globs = {'pnorm': pnorm}

    for name in []:
        suite.addTest(suiteFromPackage(name))
    for name in ['docgrok.txt', 'docgrok.py', 'objectinfo.txt', 'utilities.py']:
        suite.addTest(doctest.DocFileSuite(name,
                                           package='grok.admin',
                                           globs=globs,
                                           setUp=setUpZope,
                                           tearDown=cleanUpZope,
                                           optionflags=doctest.ELLIPSIS+
                                           doctest.NORMALIZE_WHITESPACE)
                      )
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
