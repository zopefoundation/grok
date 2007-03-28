import os
import unittest
from zope.testing import doctest
from zope.app.testing.functional import (HTTPCaller, getRootFolder,
                                         FunctionalTestSetup, sync)
from grok.testing import grok_tests, GrokFunctionalLayer

def setUp(test):
    FunctionalTestSetup().setUp()

def tearDown(test):
    FunctionalTestSetup().tearDown()

def test_suite():
    tests = grok_tests('grok.ftests',
                       layer=GrokFunctionalLayer,
                       setUp=setUp,
                       tearDown=tearDown,
                       extraglobs=dict(http=HTTPCaller(),
                                       getRootFolder=getRootFolder,
                                       sync=sync),
                       optionflags=(doctest.ELLIPSIS+
                                    doctest.NORMALIZE_WHITESPACE+
                                    doctest.REPORT_NDIFF)
                       )
    return unittest.TestSuite(tests)

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
