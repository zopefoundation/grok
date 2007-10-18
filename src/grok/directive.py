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

from zope.interface.interfaces import IInterface

from martian.error import GrokImportError
from martian.directive import (OnceDirective,
                               MultipleTimesDirective, BaseTextDirective,
                               SingleValue, SingleTextDirective,
                               MultipleTextDirective,
                               MarkerDirective,
                               InterfaceDirective,
                               InterfaceOrClassDirective,
                               ModuleDirectiveContext,
                               ClassDirectiveContext,
                               ClassOrModuleDirectiveContext)
from martian import util

class GlobalUtilityDirective(MultipleTimesDirective):
    def check_arguments(self, factory, provides=None, name=u'',
                        direct=False):
        if provides is not None and not IInterface.providedBy(provides):
            raise GrokImportError("You can only pass an interface to the "
                                  "provides argument of %s." % self.name)

    def value_factory(self, *args, **kw):
        return GlobalUtilityInfo(*args, **kw)


class GlobalUtilityInfo(object):
    def __init__(self, factory, provides=None, name=u'', direct=False):
        self.factory = factory
        self.direct = direct

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

class MultiValueOnceDirective(OnceDirective):

    def check_arguments(self, *values):
        pass

    def value_factory(self, *args):
        return args

# Define grok directives
name = SingleTextDirective('grok.name', ClassDirectiveContext())
template = SingleTextDirective('grok.template', ClassDirectiveContext())
context = InterfaceOrClassDirective('grok.context',
                                    ClassOrModuleDirectiveContext())
templatedir = SingleTextDirective('grok.templatedir', ModuleDirectiveContext())
provides = InterfaceDirective('grok.provides', ClassDirectiveContext())
baseclass = MarkerDirective('grok.baseclass', ClassDirectiveContext())
global_utility = GlobalUtilityDirective('grok.global_utility',
                                        ModuleDirectiveContext())
local_utility = LocalUtilityDirective('grok.local_utility',
                                      ClassDirectiveContext())
require = RequireDirective('grok.require', ClassDirectiveContext())
site = InterfaceOrClassDirective('grok.site',
                                 ClassDirectiveContext())
title = SingleTextDirective('grok.title', ClassDirectiveContext())
permissions = MultiValueOnceDirective(
    'grok.permissions', ClassDirectiveContext())
layer = InterfaceOrClassDirective('grok.layer',
                           ClassOrModuleDirectiveContext())
localesdir = MultipleTextDirective('grok.localesdir',
                                 ModuleDirectiveContext())
