##############################################################################
#
# Copyright (c) 2007 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Grok test helpers
"""
import sys
import os.path
import z3c.testsetup
from zope.configuration.config import ConfigurationMachine
from grokcore.component import zcml
# Provide this import here for BBB reasons:
from grokcore.component.testing import grok_component

class GrokTestCollector(z3c.testsetup.TestCollector):

    def initialize(self):
        # inject the grok ftesting ZCML as fallback...
        if 'zcml_config' in self.settings.keys():
            return
        pkg_path = os.path.dirname(self.package.__file__)
        if os.path.isfile(os.path.join(pkg_path, 'ftesting.zcml')):
            return
        self.settings['zcml_config'] = os.path.join(
            os.path.dirname(__file__), 'ftesting.zcml')
        if 'layer_name' in self.settings.keys():
            return
        self.settings['layer_name'] = 'GrokFunctionalLayer'

def register_all_tests(pkg, *args, **kw):
    return GrokTestCollector(pkg, *args, **kw)

def grok(module_name):
    config = ConfigurationMachine()
    zcml.do_grok('grokcore.component.meta', config)
    zcml.do_grok('grokcore.security.meta', config)
    zcml.do_grok('grokcore.view.meta', config)
    zcml.do_grok('grokcore.view.templatereg', config)
    zcml.do_grok('grokcore.viewlet.meta', config)
    zcml.do_grok('grokcore.formlib.meta', config)
    zcml.do_grok('grok.meta', config)
    zcml.do_grok(module_name, config)
    config.execute_actions()

def warn(message, category=None, stacklevel=1):
    """Intended to replace warnings.warn in tests.

    Modified copy from zope.deprecation.tests to:

      * make the signature identical to warnings.warn
      * to check for *.pyc and *.pyo files.

    When zope.deprecation is fixed, this warn function can be removed again.
    """
    print "From grok.testing's warn():"

    frame = sys._getframe(stacklevel)
    path = frame.f_globals['__file__']
    if path.endswith('.pyc') or path.endswith('.pyo'):
        path = path[:-1]

    file = open(path)
    lineno = frame.f_lineno
    for i in range(lineno):
        line = file.readline()

    print "%s:%s: %s: %s\n  %s" % (
        path,
        frame.f_lineno,
        category.__name__,
        message,
        line.strip(),
        )
