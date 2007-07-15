import unittest
from pkg_resources import resource_listdir
from zope.testing import doctest, cleanup

from adder import app

def cleanUpZope(test):
    cleanup.cleanUp()

def test_suite():
    suite = unittest.TestSuite()
    test = doctest.DocTestSuite(app,
                                tearDown=cleanUpZope,
                                optionflags=doctest.ELLIPSIS+
                                doctest.NORMALIZE_WHITESPACE)
    suite.addTest(test)
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
