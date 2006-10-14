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
from zope.dottedname.resolve import resolve
from zope import component

class Model(object):
    pass

class Adapter(object):

    def __init__(self, context):
        self.context = context

class GrokError(Exception):
    pass

def check_subclass(obj, class_):
    if type(obj) not in (types.ClassType, type):
        return False
    return issubclass(obj, class_)

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
            context = obj
        elif check_subclass(obj, Adapter):
            adapters.append(obj)

    if adapters and context is None:
        raise GrokError("Adapter without context")

    for factory in adapters:
        component.provideAdapter(factory, adapts=(context,))
