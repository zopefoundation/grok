##############################################################################
#
# Copyright (c) 2006 Zope Corporation and Contributors.
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
"""Grok
"""
import sys
import martian.scan

from zope import component
from zope.testing.cleanup import addCleanUp


def grok(dotted_name):
    martian.grok_dotted_name(dotted_name, the_module_grokker)

def grok_component(name, component,
                   context=None, module_info=None, templates=None):
    return the_multi_grokker.grok(name, component,
                                  context=context,
                                  module_info=module_info,
                                  templates=templates)


# The prepare hooks are executed before a module is grokked.
# Likewise, the finalize hooks are executed when a module has been
# grokked.

_prepare_hooks = set()
_finalize_hooks = set()

addPrepareHook = _prepare_hooks.add
addFinalizeHook = _finalize_hooks.add

def prepare(name, module, kw):
    module_info = martian.scan.module_info_from_module(module)
    kw['module_info'] = module_info

    for hook in _prepare_hooks:
        hook(name, module, kw)

def finalize(name, module, kw):
    for hook in _finalize_hooks:
        hook(name, module, kw)

# global grokkers
the_multi_grokker = martian.MetaMultiGrokker()
the_module_grokker = martian.ModuleGrokker(the_multi_grokker,
                                           prepare=prepare,
                                           finalize=finalize)

@addCleanUp
def resetGrokker():
    the_module_grokker.clear()
