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
"""
Views for the grok introspector.
"""

import grok
from zope.app.basicskin import IBasicSkin
from zope.app.folder.interfaces import IRootFolder
from zope.publisher.interfaces.browser import IDefaultBrowserLayer

# BBB: This will change after decoupling grok.admin from grok...
grok.context(IRootFolder)

class IntrospectorLayer(IDefaultBrowserLayer):
    """A basic layer for all introspection stuff.
    """
    pass

# This is the default layer for all views herein...
grok.layer(IntrospectorLayer)

class IntrospectorSkin(grok.Skin):
    """A skin for all introspection stuff.
    """
    grok.name('introspector')
    grok.layer(IntrospectorLayer)

class Index(grok.View):
    """The overview page.
    """
    grok.name('index.html')


# The viewlet managers...

class HeaderManager(grok.ViewletManager):
    """This viewlet manager cares for things inside the HTML header.
    """
    grok.name('header')

class PageTopManager(grok.ViewletManager):
    """This viewlet manager cares for the upper page.
    """
    grok.name('top')

class PageContentManager(grok.ViewletManager):
    """This viewlet manager cares for the main content section of a page.
    """
    grok.name('main')

class PageFooterManager(grok.ViewletManager):
    """This viewlet manager cares for the page footer.
    """
    grok.name('footer')
    
# The default viewlets...

class Overview(grok.Viewlet):
    """A default viewlet that displays an overview page.
    """
    grok.viewletmanager(PageContentManager)
    
