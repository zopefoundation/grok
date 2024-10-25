import doctest
import unittest

from pkg_resources import resource_listdir

import zope.component.eventtesting
import zope.component.testlayer
from grokcore.view.templatereg import file_template_registry
from zope.testing import cleanup

import grok
import grok.testing


class GrokTestLayer(zope.component.testlayer.LayerBase):
    def testSetUp(self):
        grok.testing.grok()
        zope.component.eventtesting.setUp()
        file_template_registry.ignore_templates(r'^\.')

    def testTearDown(self):
        cleanup.cleanUp()


layer = GrokTestLayer(grok, name='grok.tests.layer')


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
        dottedname = f'grok.tests.{name}.{filename[:-3]}'
        test = doctest.DocTestSuite(
            dottedname,
            optionflags=doctest.ELLIPSIS + doctest.NORMALIZE_WHITESPACE)
        test.layer = layer
        suite.addTest(test)
    return suite


def test_suite():
    suite = unittest.TestSuite()
    for name in [
            'adapter',
            'baseclass',
            'container',
            'directive',
            'error',
            'event',
            'grokker',
            'security',
            'traversal',
            'utility',
            'viewlet',
            'zcml'
    ]:
        suite.addTest(suiteFromPackage(name))
    return suite
