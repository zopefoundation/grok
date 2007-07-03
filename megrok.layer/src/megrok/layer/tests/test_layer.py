import unittest
from pkg_resources import resource_listdir

from grok.ftests.test_grok_functional import FunctionalDocTestSuite

from zope.app.testing import functional
functional.defineLayer('TestLayer', 'ftesting.zcml')

def suiteFromPackage(name):
    files = resource_listdir(__name__, name)
    suite = unittest.TestSuite()
    #files = ['view.py']
    for filename in files:
        if not filename.endswith('.py'):
            continue
        if filename == '__init__.py':
            continue

        dottedname = 'megrok.layer.tests.%s.%s' % (name, filename[:-3])
        test = FunctionalDocTestSuite(dottedname)
        test.layer = TestLayer

        suite.addTest(test)
    return suite

def test_suite():
    suite = unittest.TestSuite()
    s = functional.FunctionalDocFileSuite('../README.txt')
    s.layer = TestLayer
    suite.addTest(s)
    for name in ['layer']:
        suite.addTest(suiteFromPackage(name))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')

