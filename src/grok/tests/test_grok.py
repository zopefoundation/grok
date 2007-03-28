import unittest
import zope.component.eventtesting
from zope.testing import doctest, cleanup
from grok.testing import grok_tests

def setUpZope(test):
    zope.component.eventtesting.setUp(test)

def cleanUpZope(test):
    cleanup.cleanUp()

def test_suite():
    tests = grok_tests('grok.tests',
                       ignore=['.*_fixture$'],
                       setUp=setUpZope,
                       tearDown=cleanUpZope,
                       optionflags=doctest.ELLIPSIS+
                       doctest.NORMALIZE_WHITESPACE)
    return unittest.TestSuite(tests)

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
