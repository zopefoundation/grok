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
import types
import sys
from zope.dottedname.resolve import resolve
from zope import component
from zope.interface.interfaces import IInterface

class Model(object):
    pass

class Adapter(object):

    def __init__(self, context):
        self.context = context

class GrokError(Exception):
    pass

def isclass(obj):
    """We cannot use ``inspect.isclass`` because it will return True for interfaces"""
    return type(obj) in (types.ClassType, type)

def check_subclass(obj, class_):
    if not isclass(obj):
        return False
    return issubclass(obj, class_)

AMBIGUOUS_CONTEXT = object()
def grok(dotted_name):
    # TODO for now we only grok modules
    module = resolve(dotted_name)

    context = None
    adapters = []
    for name in dir(module):
        obj = getattr(module, name)

        if getattr(obj, '__module__', None) != dotted_name:
            continue

        if check_subclass(obj, Model):
            if context is None:
                context = obj
            else:
                context = AMBIGUOUS_CONTEXT
        elif check_subclass(obj, Adapter):
            adapters.append(obj)

    if getattr(module, '__grok_context__', None):
        context = module.__grok_context__

    for factory in adapters:
        adapter_context = getattr(factory, '__grok_context__', context)
        if adapter_context is None:
            raise GrokError("Adapter without context")
        elif adapter_context is AMBIGUOUS_CONTEXT:
            raise GrokError("Ambiguous contexts, please use grok.context.")
        component.provideAdapter(factory, adapts=(adapter_context,))

def context(obj):
    if not (IInterface.providedBy(obj) or isclass(obj)):
        raise GrokError("You can only pass classes or interfaces to "
                        "grok.context.")

    frame = sys._getframe(1)

    is_module = frame.f_locals is frame.f_globals
    is_class = '__module__' in frame.f_locals
    if not (is_module or is_class):
        raise GrokError("grok.context can only be used on class or module level.")

    if '__grok_context__' in frame.f_locals:
        raise GrokError("grok.context can only be called once per class "
                        "or module.")
    frame.f_locals['__grok_context__'] = obj
