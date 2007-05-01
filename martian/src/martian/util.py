##############################################################################
#
# Copyright (c) 2006-2007 Zope Corporation and Contributors.
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
"""Martian utility functions.
"""

import re
import types
import sys
import inspect

from zope import interface

from martian.error import GrokError, GrokImportError

def not_unicode_or_ascii(value):
    if isinstance(value, unicode):
        return False
    if not isinstance(value, str):
        return True
    return is_not_ascii(value)

is_not_ascii = re.compile(eval(r'u"[\u0080-\uffff]"')).search

def isclass(obj):
    """We cannot use ``inspect.isclass`` because it will return True
    for interfaces"""
    return isinstance(obj, (types.ClassType, type))


def check_subclass(obj, class_):
    if not isclass(obj):
        return False
    return issubclass(obj, class_)


def caller_module():
    return sys._getframe(2).f_globals['__name__']

def is_baseclass(name, component):
    return (type(component) is type and
            (name.endswith('Base') or
             class_annotation_nobase(component, 'grok.baseclass', False)))

def class_annotation(obj, name, default):
    return getattr(obj, '__%s__' % name.replace('.', '_'), default)

def class_annotation_nobase(obj, name, default):
    """This will only look in the given class obj for the annotation.

    It will not look in the inheritance chain.
    """
    return obj.__dict__.get('__%s__' % name.replace('.', '_'), default)
    
def class_annotation_list(obj, name, default):
    """This will process annotations that are lists correctly in the face of
    inheritance.
    """
    if class_annotation(obj, name, default) is default:
        return default

    result = []
    for base in reversed(obj.mro()):
        list = class_annotation(base, name, [])
        if list not in result:
            result.append(list)

    result_flattened = []
    for entry in result:
        result_flattened.extend(entry)
    return result_flattened

def defined_locally(obj, dotted_name):
    obj_module = getattr(obj, '__grok_module__', None)
    if obj_module is None:
        obj_module = getattr(obj, '__module__', None)
    return obj_module == dotted_name


AMBIGUOUS_CONTEXT = object()
def check_context(component, context):
    if context is None:
        raise GrokError("No module-level context for %r, please use "
                        "grok.context." % component, component)
    elif context is AMBIGUOUS_CONTEXT:
        raise GrokError("Multiple possible contexts for %r, please use "
                        "grok.context." % component, component)


def check_implements_one(class_):
    check_implements_one_from_list(list(interface.implementedBy(class_)),
                                   class_)

def check_implements_one_from_list(list, class_):
    if len(list) < 1:
        raise GrokError("%r must implement at least one interface "
                        "(use grok.implements to specify)."
                        % class_, class_)
    elif len(list) > 1:
        raise GrokError("%r is implementing more than one interface "
                        "(use grok.provides to specify which one to use)."
                        % class_, class_)


def determine_module_context(module_info, models):
    if len(models) == 0:
        context = None
    elif len(models) == 1:
        context = models[0]
    else:
        context = AMBIGUOUS_CONTEXT

    module_context = module_info.getAnnotation('grok.context', None)
    if module_context:
        context = module_context

    return context


def determine_class_context(class_, module_context):
    context = class_annotation(class_, 'grok.context', module_context)
    check_context(class_, context)
    return context


def methods_from_class(class_):
    # XXX Problem with zope.interface here that makes us special-case
    # __provides__.
    candidates = [getattr(class_, name) for name in dir(class_)
                  if name != '__provides__' ]
    methods = [c for c in candidates if inspect.ismethod(c)]
    return methods
