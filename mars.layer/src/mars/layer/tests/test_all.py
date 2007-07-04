import unittest
from pkg_resources import resource_listdir

from grok.ftests.test_grok_functional import FunctionalDocTestSuite

from zope.app.testing import functional
functional.defineLayer('TestMinimalLayer', 'minimal-ftesting.zcml')
functional.defineLayer('TestPageletLayer', 'pagelet-ftesting.zcml')

def test_suite():
    suite = unittest.TestSuite()
    dottedname = 'mars.layer.tests.%s'
    for name in ['minimal', 'directive']:
        test = FunctionalDocTestSuite(dottedname % name)
        test.layer = TestMinimalLayer
        suite.addTest(test)

    test = FunctionalDocTestSuite(dottedname % 'pagelet')
    test.layer = TestPageletLayer
    suite.addTest(test)

    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')



