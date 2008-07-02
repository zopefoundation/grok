##############################################################################
#
# Copyright (c) 2008 Zope Corporation and Contributors.
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
"""A traverser and other other central stuff for introspecting.
"""
import grok
from zope.introspector import UtilityInfo
from grok.admin.introspector.interfaces import (IGrokIntrospector,
                                                IGrokRegistryIntrospector,
                                                IGrokCodeIntrospector,
                                                IGrokZODBBrowser)

class Introspector(grok.Model):
    grok.implements(IGrokIntrospector)

    def traverse(self, path, *args, **kw):
        if path == 'registries':
            return RegistryIntrospector()
        if path == 'code':
            return CodeIntrospector()
        if path == 'zodb':
            return ZODBBrowser()
        return self

class RegistryIntrospector(grok.Model):
    grok.implements(IGrokRegistryIntrospector)

    def getUtilities(self):
        uinfo = UtilityInfo()
        return uinfo.getAllUtilities()
        

class CodeIntrospector(grok.Model):
    grok.implements(IGrokCodeIntrospector)

class ZODBBrowser(grok.Model):
    grok.implements(IGrokZODBBrowser)
