import unittest
import grok
import os.path

from pkg_resources import resource_listdir
from zope.testing import doctest
from zope.app.testing.functional import (HTTPCaller, getRootFolder,
                                         FunctionalTestSetup, sync, ZCMLLayer)

ftesting_zcml = os.path.join(os.path.dirname(grok.__file__), 'ftesting.zcml')
GrokFunctionalLayer = ZCMLLayer(ftesting_zcml, __name__, 'GrokFunctionalLayer')

def setUp(test):
    FunctionalTestSetup().setUp()

def tearDown(test):
    FunctionalTestSetup().tearDown()

def suiteFromPackage(name):
    files = resource_listdir(__name__, name)
    suite = unittest.TestSuite()
    for filename in files:
        if not filename.endswith('.py'):
            continue
        if filename == '__init__.py':
            continue

        dottedname = 'grok.ftests.%s.%s' % (name, filename[:-3])
        test = doctest.DocTestSuite(
            dottedname, setUp=setUp, tearDown=tearDown,
            extraglobs=dict(http=HTTPCaller(),
                            getRootFolder=getRootFolder,
                            sync=sync),
            optionflags=(doctest.ELLIPSIS+
                         doctest.NORMALIZE_WHITESPACE+
                         doctest.REPORT_NDIFF)
            )
        test.layer = GrokFunctionalLayer

        suite.addTest(test)
    return suite

def test_suite():
    suite = unittest.TestSuite()
    for name in ['view', 'static', 'xmlrpc', 'traversal', 'form', 'url',
                 'security', 'utility', 'catalog', 'admin']:
        suite.addTest(suiteFromPackage(name))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
