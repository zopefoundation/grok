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
"""Grok directives.
"""

import sys
import inspect
from zope import interface, component
from zope.interface.interfaces import IInterface

import grok
from grok import util
from grok.error import GrokImportError


def frame_is_module(frame):
    return frame.f_locals is frame.f_globals

def frame_is_class(frame):
    return '__module__' in frame.f_locals    

class IDirectiveContext(interface.Interface):
    description = interface.Attribute("The correct place in which the "
                                      "directive can be used.")

    def matches(frame):
        """returns whether the given frame is the correct place in
        which the directive can be used.
        """

class ClassDirectiveContext(object):
    interface.implements(IDirectiveContext)
    
    description = "class"

    def matches(self, frame):
        return frame_is_class(frame)

    
class ModuleDirectiveContext(object):
    interface.implements(IDirectiveContext)
    
    description = "module"

    def matches(self, frame):
        return frame_is_module(frame)
    
class ClassOrModuleDirectiveContext(object):
    interface.implements(IDirectiveContext)
    
    description = "class or module"

    def matches(self, frame):
        return frame_is_module(frame) or frame_is_class(frame)

class Directive(object):
    """
    Directive sets a value into the context's locals as __<name>__
    ('.' in the name are replaced with '_').
    """

    def __init__(self, name, directive_context):
        self.name = name
        self.local_name = '__%s__' % name.replace('.', '_')
        self.directive_context = directive_context

    def __call__(self, *args, **kw):
        self.check_argument_signature(*args, **kw)
        self.check_arguments(*args, **kw)

        frame = sys._getframe(1)
        self.check_directive_context(frame)

        value = self.value_factory(*args, **kw)
        return self.store(frame, value)

    def check_arguments(self, *args, **kw):
        raise NotImplementedError

    # to get a correct error message, we construct a function that has the same
    # signature as check_arguments(), but without "self".
    def check_argument_signature(self, *arguments, **kw):
        args, varargs, varkw, defaults = inspect.getargspec(self.check_arguments)
        argspec = inspect.formatargspec(args[1:], varargs, varkw, defaults)
        exec("def signature_checker" + argspec + ": pass")
        try:
            signature_checker(*arguments, **kw)
        except TypeError, e:
            message = e.args[0]
            message = message.replace("signature_checker()", self.name)
            raise TypeError(message)

    def check_directive_context(self, frame):
        if not self.directive_context.matches(frame):
            raise GrokImportError("%s can only be used on %s level."
                                  % (self.name,
                                     self.directive_context.description))

    def value_factory(self, *args, **kw):
        raise NotImplementedError

    def store(self, frame, value):
        raise NotImplementedError

class OnceDirective(Directive):
    def store(self, frame, value):
        if self.local_name in frame.f_locals:
            raise GrokImportError("%s can only be called once per %s."
                                  % (self.name,
                                     self.directive_context.description))
        frame.f_locals[self.local_name] = value

class MultipleTimesDirective(Directive):
    def store(self, frame, value):
        values = frame.f_locals.get(self.local_name, [])
        values.append(value)
        frame.f_locals[self.local_name] = values

class SingleValue(object):

    # Even though the value_factory is called with (*args, **kw), we're safe
    # since check_arguments would have bailed out with a TypeError if the number
    # arguments we were called with was not what we expect here.
    def value_factory(self, value):
        return value

class BaseTextDirective(object):
    """
    Base directive that only accepts unicode/ASCII values.
    """

    def check_arguments(self, value):
        if util.not_unicode_or_ascii(value):
            raise GrokImportError("You can only pass unicode or ASCII to "
                                  "%s." % self.name)

class SingleTextDirective(BaseTextDirective, SingleValue, OnceDirective):
    """
    Directive that accepts a single unicode/ASCII value, only once.
    """

class MultipleTextDirective(BaseTextDirective, SingleValue,
                            MultipleTimesDirective):
    """
    Directive that accepts a single unicode/ASCII value, multiple times.
    """

class InterfaceOrClassDirective(SingleValue, OnceDirective):
    """
    Directive that only accepts classes or interface values.
    """

    def check_arguments(self, value):
        if not (IInterface.providedBy(value) or util.isclass(value)):
            raise GrokImportError("You can only pass classes or interfaces to "
                                  "%s." % self.name)

class InterfaceDirective(SingleValue, OnceDirective):
    """
    Directive that only accepts interface values.
    """

    def check_arguments(self, value):
        if not (IInterface.providedBy(value)):
            raise GrokImportError("You can only pass interfaces to "
                                  "%s." % self.name)

class GlobalUtilityDirective(MultipleTimesDirective):
    def check_arguments(self, factory, provides=None, name=u''):
        if provides is not None and not IInterface.providedBy(provides):
            raise GrokImportError("You can only pass an interface to the "
                                  "provides argument of %s." % self.name)

    def value_factory(self, *args, **kw):
        return GlobalUtilityInfo(*args, **kw)

class GlobalUtilityInfo(object):
    def __init__(self, factory, provides=None, name=u''):
        self.factory = factory
        
        if provides is None:
            provides = util.class_annotation(factory, 'grok.provides', None)
        self.provides = provides
        
        if name is u'':
            name = util.class_annotation(factory, 'grok.name', u'')
        self.name = name

class LocalUtilityDirective(MultipleTimesDirective):
    def check_arguments(self, factory, provides=None, name=u'',
                        setup=None, public=False, name_in_container=None):
        if provides is not None and not IInterface.providedBy(provides):
            raise GrokImportError("You can only pass an interface to the "
                                  "provides argument of %s." % self.name)

    def value_factory(self, *args, **kw):
        return LocalUtilityInfo(*args, **kw)

class LocalUtilityInfo(object):
    def __init__(self, factory, provides=None, name=u'',
                 setup=None, public=False, name_in_container=None):
        self.factory = factory
        if provides is None:
            provides = util.class_annotation(factory, 'grok.provides', None)
        self.provides = provides
        self.name = name
        self.setup = setup
        self.public = public
        self.name_in_container = name_in_container

class RequireDirective(BaseTextDirective, SingleValue, MultipleTimesDirective):

    def store(self, frame, value):
        super(RequireDirective, self).store(frame, value)
        values = frame.f_locals.get(self.local_name, [])

        # grok.require can be used both as a class-level directive and
        # as a decorator for methods.  Therefore we return a decorator
        # here, which may be used for methods, or simply ignored when
        # used as a directive.
        def decorator(func):
            permission = values.pop()
            func.__grok_require__ = permission
            return func
        return decorator

# Define grok directives
name = SingleTextDirective('grok.name', ClassDirectiveContext())
template = SingleTextDirective('grok.template', ClassDirectiveContext())
context = InterfaceOrClassDirective('grok.context',
                                    ClassOrModuleDirectiveContext())
templatedir = SingleTextDirective('grok.templatedir', ModuleDirectiveContext())
provides = InterfaceDirective('grok.provides', ClassDirectiveContext())
global_utility = GlobalUtilityDirective('grok.global_utility',
                                        ModuleDirectiveContext())
local_utility = LocalUtilityDirective('grok.local_utility',
                                      ClassDirectiveContext())
define_permission = MultipleTextDirective('grok.define_permission',
                                          ModuleDirectiveContext())
require = RequireDirective('grok.require', ClassDirectiveContext())
