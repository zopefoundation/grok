from datetime import datetime
from docutils.core import publish_parts

import grok
from zope import schema

from blog import Blog

class Entry(grok.Model):
    class fields:
        published = schema.Datetime(title=u'Published')
        title = schema.TextLine(title=u'Title')
        body = schema.Text(title=u'Body')
        
    def __init__(self, title, body):
        self.title = title
        self.published = datetime.now()
        self.body = body

class Add(grok.View):
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

class Index(grok.View):
    grok.name('index')

    def before(self):
        self.body = renderRest(self.context.body)

class Edit(grok.View):
    grok.name('edit')

    def before(self):
        title = self.request.form.get('title', '')
        if not title:
            return
        body = self.request.form.get('body', '')
        self.context.title = title
        self.context.body = body
        self.redirect(self.url(self.context))

class Body(grok.View):
    grok.name('body')

    def render(self):
        return renderRest(self.context.body)

class Item(grok.View):
    grok.name('item')

class RandomDate(grok.View):
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

rest_settings = {'file_insertion_enabled': False}

def renderRest(source):
    return publish_parts(
        source, writer_name='html', settings_overrides=rest_settings
        )['html_body']
