import os.path
import z3c.testsetup
from zope.app.wsgi.testlayer import BrowserLayer

import sample

browser_layer = BrowserLayer(sample)

test_suite = z3c.testsetup.register_all_tests(
    'sample', globs={'getRootFolder': browser_layer.getRootFolder})
