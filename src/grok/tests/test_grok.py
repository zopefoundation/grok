import re
import unittest
import doctest
import zope.component.eventtesting
import zope.component.testlayer
import grok

from pkg_resources import resource_listdir
from zope.testing import cleanup, renormalizing
from grokcore.view.templatereg import file_template_registry

class GrokTestLayer(zope.component.testlayer.ZCMLFileLayer):
    def testSetUp(self):
        zope.component.eventtesting.setUp()
        file_template_registry.ignore_templates('^\.')

    def testTearDown(self):
        cleanup.cleanUp()

layer = GrokTestLayer(grok, zcml_file='configure.zcml')

checker = renormalizing.RENormalizing([
    # str(Exception) has changed from Python 2.4 to 2.5 (due to
    # Exception now being a new-style class).  This changes the way
    # exceptions appear in traceback printouts.
    (re.compile(r"ConfigurationExecutionError: <class '([\w.]+)'>:"),
                r'ConfigurationExecutionError: \1:'),
    ])

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
        test = doctest.DocTestSuite(
            dottedname,
            checker=checker,
            optionflags=doctest.ELLIPSIS+doctest.NORMALIZE_WHITESPACE)
        test.layer = layer
        suite.addTest(test)
    return suite

def test_suite():
    suite = unittest.TestSuite()
    for name in [
        'adapter',
        'application',
        'baseclass',
        'conflict',
        'container',
        'directive',
        'error',
        'event',
        'grokker',
        'security',
        'traversal',
        'utility',
        'viewlet',
        'xmlrpc',
        'zcml',
        ]:
        suite.addTest(suiteFromPackage(name))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
