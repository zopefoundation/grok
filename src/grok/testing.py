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
from zope.configuration.config import ConfigurationMachine
from martian import scan
from grokcore.component import zcml
import z3c.testsetup
import os.path

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

def grok_component(name, component,
                   context=None, module_info=None, templates=None):
    if module_info is None:
        obj_module = getattr(component, '__grok_module__', None)
        if obj_module is None:
            obj_module = getattr(component, '__module__', None)
        module_info = scan.module_info_from_dotted_name(obj_module)

    module = module_info.getModule()
    if context is not None:
        grokcore.component.context.set(module, context)
    if templates is not None:
        module.__grok_templates__ = templates
    config = ConfigurationMachine()
    result = zcml.the_multi_grokker.grok(name, component,
                                         module_info=module_info,
                                         config=config)
    config.execute_actions()    
    return result
