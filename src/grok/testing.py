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
from grok import zcml

def grok(module_name):
    config = ConfigurationMachine()
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
        module.__grok_context__ = context
    if templates is not None:
        module.__grok_templates__ = templates
    config = ConfigurationMachine()
    result = zcml.the_multi_grokker.grok(name, component,
                                         module_info=module_info,
                                         config=config)
    config.execute_actions()    
    return result
