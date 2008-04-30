import os.path
from zope.app.testing.functional import ZCMLLayer
from grok.testing import register_all_tests
samplelayer = ZCMLLayer(
    os.path.join(os.path.dirname(__file__), 'sample.zcml'),
    __name__, 'CustomSampleLayer')
test_suite = register_all_tests(
    'grok.tests.testsetup.cave',
    layer = samplelayer
    )
