import doctest
import importlib.resources
import importlib.util
import pathlib
import unittest

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
    try:
        with importlib.resources.as_file(
                importlib.resources.files(__name__).joinpath(name)) as path:
            filenames = [f.name for f in pathlib.Path(path).iterdir()]
    except (AttributeError, TypeError):  # PY3.11 and below
        spec = importlib.util.find_spec(__name__)
        package_path = pathlib.Path(spec.origin).parent / name
        filenames = [f.name for f in package_path.iterdir()]
    suite = unittest.TestSuite()
    for filename in filenames:
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
