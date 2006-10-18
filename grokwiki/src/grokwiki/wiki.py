import grok
import re

from zope.app import zapi

LINK_PATTERN = re.compile('\[\[(.*?)\]\]')
find_wiki_links = LINK_PATTERN.findall

from zope.app.folder.folder import Folder

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

class WikiPage(grok.Model):

    def __init__(self):
        self.text = u"GROK EMPTY WIKI PAGE. FILL!"

class Index(grok.View):
    grok.context(WikiPage)

    def before(self):
        text = self.request.form.get('wikidata')
        self.wiki = self.context.__parent__
        if text:
            links = find_wiki_links(text)
            for link in links:
                if link not in self.wiki:
                    self.wiki[link] = WikiPage()
            self.context.text = text

        wiki_url = zapi.absoluteURL(self.wiki, self.request)

        self.rendered_text, replacements = LINK_PATTERN.subn(r'<a href="%s/\1">\1</a>' % wiki_url, self.context.text)


index = grok.PageTemplate("""\
<html>
<head>
    <link rel="stylesheet" tal:attributes="href static/wiki.css" type="text/css">
</head>
<body>
<h1 tal:content="context/__name__">WikiPage</h1>

<div tal:content="structure view/rendered_text" class="wikicontent">
</div>

<hr/>

<form tal:attributes="action request/URL" method="POST">
<textarea name="wikidata" tal:content="context/text" cols="80" rows="20"/><br/>
<input type="submit" value="Update"/>
</form>

<hr/>
<h3>Other pages</h3>
<p>
    <span tal:repeat="page view/wiki">
        <a tal:attributes="href string:${view/wiki/@@absolute_url}/$page"
           tal:content="page"
           />
    </span>
</p>
</body>
</html>""")
