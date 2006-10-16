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
from zope import interface
from zope.interface.interfaces import IInterface

from grok import util
from grok.error import GrokError


def frame_is_module(frame):
    return frame.f_locals is frame.f_globals

def frame_is_class(frame):
    return '__module__' in frame.f_locals    

class IDirectiveContext(interface.Interface):
    description = interface.Attribute("The correct place in which the directive can be used.")

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
    A directive can be called only once.
    """

    def __init__(self, name, directive_context):
        self.name = name
        self.directive_context = directive_context

    def __call__(self, value):
        self.check(value)
        
        frame = sys._getframe(1)
        if not self.directive_context.matches(frame):
            raise GrokError("%s can only be used on %s level."
                            % (self.name, self.directive_context.description))
        
        local_name = '__%s__' % self.name.replace('.', '_')
        if local_name in frame.f_locals:
            raise GrokError("%s can only be called once per %s."
                            % (self.name, self.directive_context.description))
        frame.f_locals[local_name] = value

    def check(self, value):
        pass

class TextDirective(Directive):
    """
    Directive that only accepts unicode/ASCII values.
    """

    def check(self, value):
        if util.not_unicode_or_ascii(value):
            raise GrokError("You can only pass unicode or ASCII to "
                            "%s." % self.name)

class InterfaceOrClassDirective(Directive):
    """
    Directive that only accepts classes or interface values.
    """
    
    def check(self, value):
        if not (IInterface.providedBy(value) or util.isclass(value)):
            raise GrokError("You can only pass classes or interfaces to "
                            "%s." % self.name)
    
