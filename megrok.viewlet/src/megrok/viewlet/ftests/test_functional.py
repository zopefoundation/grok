import unittest
from pkg_resources import resource_listdir

from grok.ftests.test_grok_functional import FunctionalDocTestSuite

def suiteFromPackage(name):
    files = resource_listdir(__name__, name)
    suite = unittest.TestSuite()
    #files = ['view.py']
    for filename in files:
        if not filename.endswith('.py'):
            continue
        if filename == '__init__.py':
            continue

        dottedname = 'megrok.viewlet.ftests.%s.%s' % (name, filename[:-3])
        test = FunctionalDocTestSuite(dottedname)

        suite.addTest(test)
    return suite

def test_suite():
    suite = unittest.TestSuite()
    for name in ['viewlet']:
        suite.addTest(suiteFromPackage(name))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')

