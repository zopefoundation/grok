import unittest
from pkg_resources import resource_listdir

from grok.ftests.test_grok_functional import FunctionalDocTestSuite

from zope.app.testing import functional
functional.defineLayer('TestLayer', 'ftesting.zcml')

def test_suite():
    suite = unittest.TestSuite()
    dottedname = 'mars.resource.tests.%s'
    for name in ['resource']:
        test = FunctionalDocTestSuite(dottedname % name)
        test.layer = TestLayer
        suite.addTest(test)

    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')

