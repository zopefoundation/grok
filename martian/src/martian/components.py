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

from martian.interfaces import IGrokker, IComponentGrokker
from martian import util

NOT_DEFINED = object()

class GrokkerBase(object):
    implements(IGrokker)

    def grok(self, name, obj, **kw):
        raise NotImplementedError

    
class GlobalGrokker(GrokkerBase):
    """Grokker that groks once per module.
    """

    def grok(self, name, obj, **kw):
        raise NotImplementedError
    

class ComponentGrokkerBase(GrokkerBase):
    implements(IComponentGrokker)

    component_class = NOT_DEFINED

    def grok(self, name, obj, **kw):
        raise NotImplementedError


class ClassGrokker(ComponentGrokkerBase):
    """Grokker that groks classes in a module.
    """
    pass

class InstanceGrokker(ComponentGrokkerBase):
    """Grokker that groks instances in a module.
    """
    pass
