import os
import unittest
import bookshelf
from zope.testing import doctest
from zope.app.testing.functional import (FunctionalTestSetup, ZCMLLayer,
                                         HTTPCaller, sync, getRootFolder)

ftesting_zcml = os.path.join(os.path.dirname(bookshelf.__file__), 'ftesting.zcml')
BookShelfFunctionalLayer = ZCMLLayer(ftesting_zcml, __name__, 'BookShelfFunctionalLayer')

def setUp(test):
    FunctionalTestSetup().setUp()

def tearDown(test):
    FunctionalTestSetup().tearDown()

def test_suite():
    suite = unittest.TestSuite()
    test_modules = ['catalog', 'xmlrpc']

    for module in test_modules:
        module_name = 'bookshelf.ftests.%s' % module
        test = doctest.DocTestSuite(
             module_name, setUp=setUp, tearDown=tearDown,
             extraglobs=dict(http=HTTPCaller(),
                             getRootFolder=getRootFolder,
                             sync=sync),
             optionflags=(doctest.ELLIPSIS+
                          doctest.NORMALIZE_WHITESPACE+
                          doctest.REPORT_NDIFF)
             )
        test.layer = BookShelfFunctionalLayer
        suite.addTest(test)

    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
