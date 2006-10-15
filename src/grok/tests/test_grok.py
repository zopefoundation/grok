import unittest
from pkg_resources import resource_listdir
from zope.testing import doctest, cleanup

def tearDown(test):
    cleanup.cleanUp()

def grokTestSuite(pkg):
    return doctest.DocTestSuite(pkg, tearDown=tearDown,
                                optionflags=doctest.ELLIPSIS)

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
        dottedname = 'grok.tests.%s.%s' % (name, filename[:-3])
        suite.addTest(grokTestSuite(dottedname))
    return suite

def test_suite():
    suite = unittest.TestSuite()
    for name in ['adapter', 'view']:
        suite.addTest(suiteFromPackage(name))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
