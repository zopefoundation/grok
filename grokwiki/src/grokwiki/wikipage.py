import grok

from zope.app.folder.folder import Folder

class Wiki(grok.Model, Folder):
    pass

@grok.subscribe(Wiki, grok.IObjectAddedEvent)
def setupHomepage(wiki, event):
    page = WikiPage()
    wiki['home'] = page

class WikiPage(grok.Model):

    def __init__(self):
        self.text = u"GROK EMPTY WIKI PAGE. FILL!"

grok.context(WikiPage)

class Index(grok.View):

    def before(self):
        text = self.request.form.get('wikidata')
        if text:
            self.context.text = text

index = grok.PageTemplate("""\
<html>
<body>
<form action=".">
<textarea name="wikidata" tal:content="context/text"/><br/>
<input type="submit"/>
</form>
</body>
</html>""")
