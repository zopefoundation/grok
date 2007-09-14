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
"""Essential directives that are needed for the most basic component
registrations
"""
from martian.directive import SingleTextDirective
from martian.directive import InterfaceDirective
from martian.directive import InterfaceOrClassDirective
from martian.directive import ClassDirectiveContext
from martian.directive import ClassOrModuleDirectiveContext

name = SingleTextDirective('grok.name', ClassDirectiveContext())
context = InterfaceOrClassDirective('grok.context',
                                    ClassOrModuleDirectiveContext())
provides = InterfaceDirective('grok.provides', ClassDirectiveContext())
