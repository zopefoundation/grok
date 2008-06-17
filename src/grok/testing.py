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
import os.path
import z3c.testsetup
import grokcore.component
from zope.configuration.config import ConfigurationMachine
from martian import scan
from grokcore.component import zcml
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
    zcml.do_grok('grok.meta', config)
    zcml.do_grok('grok.templatereg', config)
    zcml.do_grok(module_name, config)
    config.execute_actions()
