import unittest
from pkg_resources import resource_listdir

from grok.ftests.test_grok_functional import FunctionalDocTestSuite

from zope.app.testing import functional

from martian.tests.test_all import globs, optionflags

functional.defineLayer('TestLayer', 'ftesting.zcml')

def suiteFromPackage(name):
    files = resource_listdir(__name__, name)
    suite = unittest.TestSuite()
    for filename in files:
        if not filename.endswith('.py'):
            continue
        if filename == '__init__.py':
            continue
        if filename == 'test_all.py':
            continue

        dottedname = 'mars.template.tests.%s' % (filename[:-3])
        test = FunctionalDocTestSuite(dottedname)
        test.layer = TestLayer

        suite.addTest(test)
    return suite

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(suiteFromPackage('.'))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')


