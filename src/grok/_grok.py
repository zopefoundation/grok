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
from zope import interface
from zope.interface.interfaces import IInterface
from zope.publisher.browser import BrowserPage
from zope.publisher.interfaces.browser import IDefaultBrowserLayer

class Model(object):
    pass

class Adapter(object):

    def __init__(self, context):
        self.context = context

class View(BrowserPage):

    def __call__(self):
        return self.render()

    def render(self):
        raise NotImplemented

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
    views = []
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
        elif check_subclass(obj, View):
            views.append(obj)

    if getattr(module, '__grok_context__', None):
        context = module.__grok_context__

    for factory in adapters:
        adapter_context = determineContext(factory, context)
        component.provideAdapter(factory, adapts=(adapter_context,))

    for factory in views:
        view_context = determineContext(factory, context)
        name = factory.__name__.lower()
        name = getattr(factory, '__grok_name__', name)
        component.provideAdapter(factory,
                                 adapts=(view_context, IDefaultBrowserLayer),
                                 provides=interface.Interface,
                                 name=name)

def determineContext(factory, module_context):
    context = getattr(factory, '__grok_context__', module_context)
    if context is None:
        raise GrokError("Cannot determine context for %r, please use "
                        "grok.context." % factory)
    elif context is AMBIGUOUS_CONTEXT:
        raise GrokError("Ambiguous contexts for %r, please use "
                        "grok.context." % factory)
    return context

def caller_is_module():
    frame = sys._getframe(2)
    return frame.f_locals is frame.f_globals

def caller_is_class():
    frame = sys._getframe(2)
    return '__module__' in frame.f_locals

def set_local(name, value, error_message):
    frame = sys._getframe(2)
    name = '__grok_%s__' % name
    if name in frame.f_locals:
        raise GrokError(error_message)
    frame.f_locals[name] = value
    
def context(obj):
    if not (IInterface.providedBy(obj) or isclass(obj)):
        raise GrokError("You can only pass classes or interfaces to "
                        "grok.context.")
    if not (caller_is_module() or caller_is_class()):
        raise GrokError("grok.context can only be used on class or module level.")
    set_local('context', obj, "grok.context can only be called once per class "
              "or module.")

def name(name):
    if not caller_is_class():
        raise GrokError("grok.name can only be used on class level.")
    set_local('name', name, "grok.name can only be called once per class.")
