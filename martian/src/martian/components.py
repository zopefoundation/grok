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

from zope.interface import implements

from martian.interfaces import IMartian, IComponentMartian
from martian import util

NOT_DEFINED = object()

class MartianBase(object):
    implements(IMartian)
    
    priority = 0
    continue_scanning = False

    def match(self, name, obj):
        raise NotImplementedError

    def grok(self, name, obj, **kw):
        raise NotImplementedError

    
class GlobalMartian(MartianBase):
    """Martian that groks once per module.
    """

    def match(self, name, obj):
        # we never match with any object
        return False

    def grok(self, name, obj, **kw):
        raise NotImplementedError
    

class ComponentMartianBase(MartianBase):
    implements(IComponentMartian)

    component_class = NOT_DEFINED

    def grok(self, name, obj, **kw):
        raise NotImplementedError


class ClassMartian(ComponentMartianBase):
    """Martian that groks classes in a module.
    """
    def match(self, name, obj):
        return util.check_subclass(obj, self.component_class)


class InstanceMartian(ComponentMartianBase):
    """Martian that groks instances in a module.
    """
    def match(self, name, obj):
        return isinstance(obj, self.component_class)
