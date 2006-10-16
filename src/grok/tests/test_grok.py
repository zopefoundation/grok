import unittest
from pkg_resources import resource_listdir
from zope.testing import doctest, cleanup

def cleanUpZope(test):
    cleanup.cleanUp()

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
        test = doctest.DocTestSuite(dottedname, tearDown=cleanUpZope,
                                    optionflags=doctest.ELLIPSIS+
                                    doctest.NORMALIZE_WHITESPACE)

        suite.addTest(test)
    return suite

def test_suite():
    suite = unittest.TestSuite()
    for name in ['adapter', 'view', 'security']:
        suite.addTest(suiteFromPackage(name))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
