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
"""The grok demo wiki
"""

import grok
import grokwiki.page

class Wiki(grok.Container):
    """This is our wiki application wich contains all wiki pages."""

    @grok.traverse
    def getWikiPage(self, name):
        # XXX This should be the default of grok.Container
        return self[name]

class WikiIndex(grok.View):
    grok.name('index')

    def render(self):
        self.redirect(self.url('home'))

@grok.subscribe(Wiki, grok.IObjectAddedEvent)
def setupHomepage(wiki, event):
    """Creates a home page for every wiki."""
    page = grokwiki.page.WikiPage()
    wiki['home'] = page
