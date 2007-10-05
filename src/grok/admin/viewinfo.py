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
"""
"""

from zope.interface import Interface, providedBy
from zope import component
from zope.publisher.browser import BrowserRequest

import grok

class IViewInfo(Interface):

    def getViews():
        """Return a list of views available on the context.
        """


class ViewInfo(grok.Adapter):
    """Determine views for contexts.
    """
    grok.provides(IViewInfo)
    grok.context(Interface)

    def getViews(self):
        """Return a list of tuples with a view name and a view
        factory.
        """
        request = BrowserRequest(None, {})
        sm = component.getSiteManager()
        return sm.adapters.lookupAll(map(providedBy, (self.context, request)),
                              Interface)
        
