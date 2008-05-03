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
"""Grok directives.
"""

import grok
from zope.interface.interfaces import IInterface
from zope.publisher.interfaces.browser import IBrowserView

from martian.error import GrokImportError
from martian.directive import (Directive, OnceDirective,
                               MultipleTimesDirective, BaseTextDirective,
                               SingleValue, SingleTextDirective,
                               MultipleTextDirective,
                               MarkerDirective,
                               InterfaceDirective,
                               InterfaceOrClassDirective,
                               ModuleDirectiveContext,
                               OptionalValueDirective,
                               ClassDirectiveContext,
                               ClassOrModuleDirectiveContext)
from martian import util
from martian import ndir
from grok import components

class MultiValueOnceDirective(OnceDirective):

    def check_arguments(self, *values):
        pass

    def value_factory(self, *args):
        return args

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


class MultipleTimesAsDictDirective(Directive):
    def store(self, frame, value):
        values = frame.f_locals.get(self.local_name, {})
        values[value[1]] = value[0]
        frame.f_locals[self.local_name] = values


class RequireDirective(SingleValue, MultipleTimesDirective):
    def check_arguments(self, value):
        if util.check_subclass(value, components.Permission):
            return
        if util.not_unicode_or_ascii(value):
            raise GrokImportError(
                "You can only pass unicode, ASCII, or a subclass "
                "of grok.Permission %s." % self.name)

    def store(self, frame, value):
        if util.check_subclass(value, components.Permission):
            value = grok.name.get(value)

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
template = SingleTextDirective('grok.template', ClassDirectiveContext())
templatedir = SingleTextDirective('grok.templatedir', ModuleDirectiveContext())
local_utility = LocalUtilityDirective('grok.local_utility',
                                      ClassDirectiveContext())
require = RequireDirective('grok.require', ClassDirectiveContext())
site = InterfaceOrClassDirective('grok.site',
                                 ClassDirectiveContext())

class permissions(ndir.Directive):
    scope = ndir.CLASS
    store = ndir.ONCE
    default = []

    def factory(*args):
        return args

class OneInterfaceOrClassOnClassOrModule(ndir.Directive):
    scope = ndir.CLASS_OR_MODULE
    store = ndir.ONCE
    validate = ndir.validateInterfaceOrClass

class layer(OneInterfaceOrClassOnClassOrModule):
    pass

class viewletmanager(OneInterfaceOrClassOnClassOrModule):
    pass

class view(OneInterfaceOrClassOnClassOrModule):
    default = IBrowserView

class traversable(ndir.Directive):
    scope = ndir.CLASS
    store = ndir.DICT

    def factory(self, attr, name=None):
        if name is None:
            name = attr
        return (name, attr)
