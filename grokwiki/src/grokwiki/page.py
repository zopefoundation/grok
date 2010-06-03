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
import re
import grok

from z3c.flashmessage.interfaces import IMessageReceiver
from zope import component

LINK_PATTERN = re.compile('\[\[(.*?)\]\]')
find_wiki_links = LINK_PATTERN.findall


class WikiPage(grok.Model):

    def __init__(self):
        self.text = u"GROK EMPTY WIKI PAGE. FILL!"

    def update(self, text):
        links = find_wiki_links(text)
        for link in links:
            if link not in self.__parent__:
                self.__parent__[link] = WikiPage()
        self.text = text


class Layout(grok.View):
    pass


class Index(grok.View):

    def update(self):
        wiki_url = self.url(self.context.__parent__)
        self.rendered_text, replacements = (
            LINK_PATTERN.subn(r'<a href="%s/\1">\1</a>' % wiki_url, 
                              self.context.text))

class Edit(grok.View):

    def update(self):
        text = self.request.form.get('wikidata')
        if not text:
            return # Just render the template

        # Update the text and redirect
        self.context.update(text)
        self.flash('Saved.')
        self.redirect(self.url(self.context))

class Messages(grok.View):
    @property
    def messages(self):
        receiver = component.getUtility(IMessageReceiver)
        return receiver.receive()

class WikiLayer(grok.IRESTLayer):
    # This skin will be visible as http://localhost:8080/++rest++wiki/...
    grok.restskin('wiki')

class PageRest(grok.REST):
    grok.layer(WikiLayer)
    
    def GET(self):
        return "Hello world"
