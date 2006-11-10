import random
from datetime import datetime, timedelta
from docutils.core import publish_parts
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
    published = schema.Datetime(title=u'Published')
    title = schema.TextLine(title=u'Title')
    body = schema.Text(title=u'Body')

class Entry(grok.Model):
    interface.implements(IEntry)

    def __init__(self, title, body):
        self.title = title
        self.published = datetime.now()
        self.body = body

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

class YearIndex(grok.View):
    grok.name('index')
    grok.context(Year)
    grok.template('dateindex')

    def entries(self):
        from_ = datetime(self.context.year, 1, 1)
        until = datetime(self.context.year + 1, 1, 1)
        return entriesInDateRange(from_, until)

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

class MonthIndex(grok.View):
    grok.name('index')
    grok.context(Month)
    grok.template('dateindex')

    def entries(self):
        from_ = datetime(self.context.year,
                         self.context.month,
                         1)
        month = self.context.month + 1
        year = self.context.year
        if month > 12:
            month = 1
            year += 1
        until = datetime(year, month, 1)
        return entriesInDateRange(from_, until)

class Day(grok.Model):
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

class DayIndex(grok.View):
    grok.name('index')
    grok.context(Day)
    grok.template('dateindex')

    def entries(self):
        from_ = datetime(self.context.year,
                         self.context.month,
                         self.context.day)
        until = from_ + timedelta(days=1)
        return entriesInDateRange(from_, until)

def entriesInDateRange(from_, until):
    entries = grok.getSite()['entries']
    result = []
    for entry in entries.values():
        if from_ <= entry.published <= until:
            result.append(entry)
    return sorted(
        result, key=lambda entry: entry.published, reverse=True
        )

def lastEntries(amount):
    entries = grok.getSite()['entries'].values()
    return sorted(
        entries, key=lambda entry: entry.published, reverse=True
        )[:amount]

class BlogIndex(grok.View):
    grok.context(Blog)
    grok.name('index')

    def entries(self):
        return lastEntries(10)

    def renderEntry(self, entry):
        return renderRest(entry.body)

class AddEntry(grok.View):
    grok.context(Blog)
    grok.name('add')

    def before(self):
        id = self.request.form.get('id')
        if not id:
            return
        title = self.request.form.get('title', '')
        body = self.request.form.get('body', '')
        self.context['entries'][id] = Entry(title, body)
        self.redirect(self.url(self.context))

class EntriesIndex(grok.View):
    grok.context(Entries)
    grok.name('index')

    def render(self):
        return "Entries: %s" % ' '.join(self.context.keys())

rest_settings = {'file_insertion_enabled': False}

def renderRest(source):
    return publish_parts(
        source, writer_name='html', settings_overrides=rest_settings
        )['html_body']

class EntryIndex(grok.View):
    grok.context(IEntry)
    grok.name('index')

    def before(self):
        self.body = renderRest(self.context.body)

class EntryEdit(grok.View):
    grok.context(IEntry)
    grok.name('edit')

    def before(self):
        title = self.request.form.get('title', '')
        if not title:
            return
        body = self.request.form.get('body', '')
        self.context.title = title
        self.context.body = body
        self.redirect(self.url(self.context))

class EntryBody(grok.View):
    grok.context(IEntry)
    grok.name('body')

    def render(self):
        return renderRest(self.context.body)

class EntryItem(grok.View):
    grok.context(IEntry)
    grok.name('item')

class EntryRandomDate(grok.View):
    grok.context(IEntry)
    grok.name('random_date')

    def render(self):
        self.context.published = datetime(
            2006,
            11,
            random.randrange(1, 29),
            random.randrange(0, 24),
            random.randrange(0, 60),
            )
        return str(self.context.published)
