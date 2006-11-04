from datetime import datetime, timedelta
import grok

from zope import interface, schema

class Blog(grok.Container, grok.Site):
    def __init__(self):
        super(Blog, self).__init__()
        self['entries'] = Entries()

    def traverse(self, name):
        try:
            year = int(name)
        except ValueError:
            return None
        return Year(year)
    
class Entries(grok.Container):
    pass

class IEntry(interface.Interface):
    title = schema.TextLine(title=u'Title')
    published = schema.Datetime(title=u'Published')
    
class Entry(grok.Model):
    interface.implements(IEntry)

    def __init__(self, title):
        self.title = title
        self.published = datetime.now()

class Year(grok.Model):
    def __init__(self, year):
        self.year = year
        
    def traverse(self, name):
        try:
            month = int(name)
        except ValueError:
            return None
        if month < 1 or month > 12:
            return None
        return Month(self.year, month)

class Month(grok.Model):
    def __init__(self, year, month):
        self.year = year
        self.month = month
        
    def traverse(self, name):
        try:
            day = int(name)
        except ValueError:
            return None
        # XXX should check whether day is acceptable
        return Day(self.year, self.month, day)

class Day(grok.Model):
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

class DayIndex(grok.View):
    grok.name('index')
    grok.context(Day)
    
    def render(self):
        from_ = datetime(self.context.year,
                         self.context.month,
                         self.context.day)
        until = from_ + timedelta(days=1)
        entries = entriesInDateRange(from_, until)
        return "Entries: %s" % ' '.join([entry.__name__ for entry in entries])

def entriesInDateRange(from_, until):
    entries = grok.getSite()['entries']
    for entry in entries.values():
        if from_ <= entry.published <= until:
            yield entry
       
class BlogIndex(grok.View):
    grok.context(Blog)
    grok.name('index')

blogindex = grok.PageTemplate('''\
<html>
<body>
<form tal:attributes="action python:view.url('add_entry')" method="POST">
id: <input type="text" name="id" value="" /><br />
title: <input type="text" name="title" value="" /><br />
<input type="submit" value="Add Entry" />
</form>
</body>
</html>
''')

class AddEntry(grok.View):
    grok.context(Blog)
    grok.name('add_entry')

    def render(self):
        id = self.request.form.get('id')
        title = self.request.form.get('title', '')
        if id:
            self.context['entries'][id] = Entry(title)
        self.redirect(self.url(self.context))
        
class EntriesIndex(grok.View):
    grok.context(Entries)
    grok.name('index')

    def render(self):
        return "Entries: %s" % ' '.join(self.context.keys())
    
class EntryIndex(grok.View):
    grok.context(IEntry)
    grok.name('index')

    def render(self):
        return "Title: %s" % self.context.title
    
