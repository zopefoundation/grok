"""
A form view can completely override which fields are displayed by setting
form_fields manually:

  >>> grok.grok(__name__)

We need to set up the default formlib template first, because even though we
don't use the formlib NamedTemplates directly they need to be present to create
a formlib form.

  >>> from zope import component
  >>> from zope.formlib import form
  >>> component.provideAdapter(form.default_page_template, name='default')

  >>> from zope.publisher.browser import TestRequest
  >>> request = TestRequest()

We only expect a single field to be present in the form, as we omitted 'size':

  >>> view = component.getMultiAdapter((Mammoth(), request), name='edit')
  >>> len(view.form_fields)
  1
  >>> [w.__name__ for w in view.form.form_fields]
  ['name']

"""

import grok
from zope import interface, schema

class IMammoth(interface.Interface):
    name = schema.TextLine(title=u"Name")
    size = schema.TextLine(title=u"Size", default=u"Quite normal")

class Mammoth(grok.Model):
    interface.implements(IMammoth)

class Edit(grok.EditForm):
    grok.context(Mammoth)

    form_fields = grok.Fields(IMammoth).omit('size')
