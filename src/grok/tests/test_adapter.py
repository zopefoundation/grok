import unittest
from pkg_resources import resource_listdir
from zope.testing import doctest, cleanup

def tearDown(test):
    cleanup.cleanUp()

def grokTestSuite(pkg):
    return doctest.DocTestSuite(pkg, tearDown=tearDown,
                                optionflags=doctest.ELLIPSIS)

def test_suite():
    adapterfiles = resource_listdir(__name__, 'adapter')
    suite = unittest.TestSuite()
    for filename in adapterfiles:
        if not filename.endswith('.py'):
            continue
        if filename.endswith('_fixture.py'):
            continue
        if filename == '__init__.py':
            continue
        dottedname = 'grok.tests.adapter.' + filename[:-3]
        suite.addTest(grokTestSuite(dottedname))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
