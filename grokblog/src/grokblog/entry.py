from datetime import datetime
import random
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

class Add(grok.AddForm):
    grok.context(Blog)

    form_fields = grok.Fields(
        id=schema.TextLine(title=u"id"))
    form_fields += grok.AutoFields(Entry).omit('published')

    @grok.action('Add entry')
    def add(self, id, title, body):
        self.context['entries'][id] = Entry(title, body)
        self.redirect(self.url(self.context))

class Index(grok.View):

    def before(self):
        self.body = renderRest(self.context.body)

class Edit(grok.EditForm):

    form_fields = grok.AutoFields(Entry).omit('published')

    @grok.action('Save changes')
    def edit(self, **data):
        self.applyChanges(**data)
        self.redirect(self.url(self.context))

class Body(grok.View):

    def render(self):
        return renderRest(self.context.body)

class RandomDate(grok.View):
    # for testing purposes

    def render(self):
        self.context.published = datetime(
            2006,
            11,
            random.randrange(1, 29),
            random.randrange(0, 24),
            random.randrange(0, 60),
            )
        return str(self.context.published)

rest_settings = {
    # Disable inclusion of external files, which is a security risk.
    'file_insertion_enabled': False,
    # Disable the promotion of a lone top-level section title to document title
    # (and disable the promotion of a subsequent section title to document
    # subtitle).
    'doctitle_xform': False
    }

def renderRest(source):
    return publish_parts(
        source, writer_name='html', settings_overrides=rest_settings
        )['html_body']
