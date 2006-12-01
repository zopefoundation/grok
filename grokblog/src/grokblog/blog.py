import random
from datetime import datetime, timedelta
import grok

class Blog(grok.Container, grok.Site):
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

