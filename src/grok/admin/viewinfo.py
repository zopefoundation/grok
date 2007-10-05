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

from zope.interface import Interface, providedBy, alsoProvides
from zope import component
from zope.publisher.browser import BrowserRequest
from zope.publisher.interfaces.browser import (IBrowserSkinType,
                                               IDefaultBrowserLayer)
                                               
import grok

class IViewInfo(Interface):

    def getViews(layer=None):
        """Get the views for context object.

        Optional layer argument retrieves views registered for this layer.

        Returns iterator (view name, view factory) tuples.
        """


    def getAllViews():
        """Get all views for context objects, for any layer that is in a skin.

        Returns iterator of (skin name, (skin) layer, view name,
        view factory) tuples.

        The default layer will be returned with u'' as the skin name.
        """
        
class ViewInfo(grok.Adapter):
    """Determine views for contexts.
    """
    grok.provides(IViewInfo)
    grok.context(Interface)

    def getViews(self, layer=None):
        request = BrowserRequest(None, {})
        if layer is not None:
            alsoProvides(request, layer)
        sm = component.getSiteManager()
        return sm.adapters.lookupAll(
            map(providedBy, (self.context, request)),
            Interface)
        
    def getAllViews(self):
        for skin_name, layer in getSkins():
            for view_name, factory in self.getViews(layer):
                yield skin_name, layer, view_name, factory
        for view_name, factory in self.getViews(IDefaultBrowserLayer):
            yield u'', IDefaultBrowserLayer, view_name, factory 
            
def getSkins():
    """Get all the skins registered in the system.
    """
    return component.getUtilitiesFor(IBrowserSkinType)

