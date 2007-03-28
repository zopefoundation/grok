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
"""
Grok testing facilities
"""
import re
from zope.testing import doctest
from grok import util, components, grokker, scan

class DocTestGrokker(components.ModuleGrokker):

    def __init__(self, **defaults):
        self.defaults = defaults

    def register(self, context, module_info, templates):
        global found_tests

        module = module_info.getModule()
        options = util.class_annotation(module, 'grok.doctest', {})

        options_w_defaults = self.defaults.copy()
        options_w_defaults.update(options)
        layer = options_w_defaults.pop('layer', None)

        try:
            suite = doctest.DocTestSuite(module_info.dotted_name,
                                         **options_w_defaults)
        except ValueError:
            # The module contains no tests. That's fine, just skip it
            return # XXX but not when grok.doctest() is called explicitly

        if layer is not None:
            suite.layer = layer
        found_tests.append(suite)

found_tests = []
def grok_tests(dotted_name, ignore=[], **defaults):
    global found_tests
    ignore = [re.compile(expr).match for expr in ignore]

    # Create a separate grokker registry just for the test grokker so
    # separate concerns between test finding code and testing code
    test_grokker_registry = grokker.GrokkerRegistry()
    test_grokker_registry.registerGrokker(DocTestGrokker(**defaults))
    module_info = scan.module_info_from_dotted_name(dotted_name)
    grok_tree(test_grokker_registry, module_info, ignore)

    # Make sure we clear the global list of tests before returning
    # them (so that subsequent calls to this function don't end up
    # returning old results as well)
    return_tests, found_tests[:] = found_tests[:], []
    return return_tests

def grok_tree(registry, module_info, ignore):
    for ignore_match in ignore:
        if ignore_match(module_info.dotted_name):
            return

    registry.grok(module_info)

    for sub_module_info in module_info.getSubModuleInfos():
        grok_tree(registry, sub_module_info, ignore)
