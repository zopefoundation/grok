##############################################################################
#
# Copyright (c) 2006 Zope Foundation and Contributors.
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
"""The grok demo wiki
"""

import grok
import grokwiki.page

class Wiki(grok.Application, grok.Container):
    """This is Grok's sample wiki application."""

class Index(grok.View):
    def render(self):
        self.redirect(self.url('home'))

class Hello(grok.View):
    grok.baseclass()
    
    def render(self):
        return "Hello"

class Hoi(Hello):
    def render(self):
        return "Hoi"

class Bonjour(Hello):
    def render(self):
        return "Bonjour"

@grok.subscribe(Wiki, grok.IObjectAddedEvent)
def setupHomepage(wiki, event):
    """Creates a home page for every wiki."""
    page = grokwiki.page.WikiPage()
    wiki['home'] = page
