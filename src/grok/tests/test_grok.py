import re
import unittest
import doctest
import zope.component.eventtesting
import zope.component.testlayer
import grok
import grok.testing

from pkg_resources import resource_listdir
from zope.testing import cleanup, renormalizing
from grokcore.view.templatereg import file_template_registry

class GrokTestLayer(zope.component.testlayer.LayerBase):
    def testSetUp(self):
        grok.testing.grok()
        zope.component.eventtesting.setUp()
        file_template_registry.ignore_templates('^\.')

    def testTearDown(self):
        cleanup.cleanUp()

layer = GrokTestLayer(grok, name='grok.tests.layer')

checker = renormalizing.RENormalizing([
    (re.compile(
        r'zope.interface.interfaces.ComponentLookupError: '),
        'ComponentLookupError: '),
    (re.compile(
        r'martian.error.GrokImportError: '),
        'GrokImportError: '),
    (re.compile(
        r"<class 'martian.error.GrokError'>: "),
        "GrokError: "),
    (re.compile(
        r'martian.error.GrokError: '),
        'GrokError: '),
    (re.compile(
        r'zope.configuration.config.ConfigurationConflictError: '),
        'ConfigurationConflictError: '),
    (re.compile(
        r'zope.configuration.xmlconfig.ZopeXMLConfigurationError: '),
        'ZopeXMLConfigurationError: '),
    (re.compile(
        r'zope.configuration.config.ConfigurationExecutionError: '),
        'ConfigurationExecutionError: '),
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
            extraglobs={
                'print': grok.testing.bprint,
            },
            optionflags=doctest.ELLIPSIS+doctest.NORMALIZE_WHITESPACE)
        test.layer = layer
        suite.addTest(test)
    return suite

def test_suite():
    suite = unittest.TestSuite()
    for name in [
        'adapter',
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
