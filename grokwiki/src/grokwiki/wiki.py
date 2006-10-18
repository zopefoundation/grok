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
import re

from zope.app import zapi
from zope.app.folder.folder import Folder

import grok


LINK_PATTERN = re.compile('\[\[(.*?)\]\]')
find_wiki_links = LINK_PATTERN.findall


# First: The wiki application

class Wiki(grok.Model, Folder):
    pass


class WikiIndex(grok.View):
    grok.context(Wiki)
    grok.name('index')

    def render(self):
        self.request.response.redirect('home')


@grok.subscribe(Wiki, grok.IObjectAddedEvent)
def setupHomepage(wiki, event):
    page = WikiPage()
    wiki['home'] = page


# Second: The wiki page

class WikiPage(grok.Model):

    def __init__(self):
        self.text = u"GROK EMPTY WIKI PAGE. FILL!"

grok.context(WikiPage)


class Index(grok.View):

    def before(self):
        wiki_url = zapi.absoluteURL(self.context.__parent__, self.request)
        self.rendered_text, replacements = (
            LINK_PATTERN.subn(r'<a href="%s/\1">\1</a>' % wiki_url, 
                              self.context.text))


index = grok.PageTemplate("""\
<html metal:use-macro="context/@@layout/main">
    <div metal:fill-slot="content">
        <h1 tal:content="context/__name__">WikiPage</h1>

        <div tal:content="structure view/rendered_text" class="wikicontent">
        </div>

        <p><a tal:attributes="href string:${context/@@absolute_url}/edit">Edit this page</a></p>
    </div>
</html>""")


layout = grok.PageTemplate("""\
<html metal:define-macro="main">
    <head>
        <link rel="stylesheet" tal:attributes="href static/wiki.css" type="text/css">
    </head>

    <body
        tal:define="wiki context/__parent__;
                    wiki_url wiki/@@absolute_url">
        <div metal:define-slot="content">
            Page content goes here ...
        </div>

        <hr/>
        <h3>Other pages</h3>
        <p>
            <span tal:repeat="page wiki">
                <a tal:attributes="href string:$wiki_url/$page"
                   tal:content="page"
                   />
            </span>
        </p>
        <hr/>
        <div id="footer">
        This Wiki was grokked by Zope 3.
        </div>
    </body>
</html>""")


class Edit(grok.View):

    def before(self):
        text = self.request.form.get('wikidata')
        self.wiki = self.context.__parent__
        if not text:
            return  # Just render the template

        # Update the text and redirect
        links = find_wiki_links(text)
        for link in links:
            if link not in self.wiki:
                self.wiki[link] = WikiPage()
        self.context.text = text
        wiki_url = zapi.absoluteURL(self.wiki, self.request)
        self.request.response.redirect("%s/%s" % (wiki_url, self.context.__name__))


edit = grok.PageTemplate("""\
<html metal:use-macro="context/@@layout/main">
    <div metal:fill-slot="content">
        <h1>Edit &raquo;<span tal:replace="context/__name__">WikiPage</span>&laquo;</h1>

        <form tal:attributes="action request/URL" method="POST">
        <textarea name="wikidata" tal:content="context/text" cols="80" rows="20"/><br/>
        <input type="submit" value="Update"/>
        </form>
    </div>
</html>""")
