import os.path
from grok.testing import register_all_tests
test_suite = register_all_tests(
    'grok.tests.testsetup.cave',
    zcml_config = os.path.join(os.path.dirname(__file__),
                               'sample.zcml'),
    layer_name = 'CustomLayerFromPath')

