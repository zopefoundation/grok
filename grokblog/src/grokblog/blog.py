import random
from datetime import datetime, timedelta

from zope import schema

import grok

class Blog(grok.Container, grok.Site):

    class fields:
        title = schema.TextLine(title=u'Title', default=u'')
        tagline = schema.TextLine(title=u'Tagline', default=u'')

    def __init__(self):
        super(Blog, self).__init__()
        self['entries'] = Entries()

class Entries(grok.Container):
    pass

class BlogIndex(grok.View):
    grok.context(Blog)
    grok.name('index')

    def entries(self):
        return lastEntries(10)

    def renderEntry(self, entry):
        return renderRest(entry.body)

class BlogEdit(grok.EditForm):
    grok.context(Blog)
    grok.name('edit')

    @grok.action('Save changes')
    def edit(self, **data):
        self.applyChanges(**data)
        self.redirect(self.url(self.context))

class EntriesIndex(grok.View):
    grok.context(Entries)
    grok.name('index')

    def render(self):
        return "Entries: %s" % ' '.join(self.context.keys())

def lastEntries(amount):
    entries = grok.getSite()['entries'].values()
    return sorted(
        entries, key=lambda entry: entry.published, reverse=True
        )[:amount]
