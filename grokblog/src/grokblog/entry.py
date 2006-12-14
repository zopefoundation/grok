from datetime import datetime
from docutils.core import publish_parts

from zope import schema, interface

import grok

from grokblog.blog import Blog
from grokblog import interfaces

class Entry(grok.Model):
    interface.implements(interfaces.IEntry)

    def __init__(self, title, summary, rightsinfo):
        self.title = title
        self.updated = datetime.now()
        self.published = datetime.now()
        self.summary = summary
        self.rightsinfo = rightsinfo
        
class RestructuredTextEntry(Entry):
    interface.implements(interfaces.IRestructuredTextEntry)

    def __init__(self, title, summary, rightsinfo, content):
        super(RestructuredTextEntry, self).__init__(title, summary, rightsinfo)
        self.content = content

grok.context(RestructuredTextEntry)

class AddRest(grok.AddForm):
    grok.context(Blog)

    form_fields = grok.Fields(
        id=schema.TextLine(title=u"id"))
    form_fields += grok.AutoFields(RestructuredTextEntry).omit(
        'published', 'updated')

    @grok.action('Add entry')
    def add(self, id, **data):
        self.context['entries'][id] = RestructuredTextEntry(**data)
        self.redirect(self.url(self.context))

class Edit(grok.EditForm):
    form_fields = grok.AutoFields(RestructuredTextEntry).omit(
        'published', 'updated')

    @grok.action('Save changes')
    def edit(self, **data):
        self.applyChanges(**data)
        self.redirect(self.url(self.context))

class RenderedContent(grok.View):
    def render(self):
        return renderRest(self.context.content)

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
