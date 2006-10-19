"""
A grok.Model may contain a nested class named 'fields'. All attributes of
'fields' that provide IField will cause attributes of the same name to appear on
the grok.Model:

  >>> grok.grok(__name__)
  >>> manfred = Mammoth()
  >>> print manfred.name
  None
  >>> print manfred.size
  Quite normal
  >>> manfred.somethingelse
  Traceback (most recent call last):
    ...
  AttributeError: 'Mammoth' object has no attribute 'somethingelse'

A grok.EditForm is a special grok.View that renders an edit form.

We need to set up the default formlib template first, because even though we
don't use the formlib NamedTemplates directly they need to be present to create
a formlib form.

  >>> from zope import component
  >>> from zope.formlib import form
  >>> component.provideAdapter(form.default_page_template, name='default')

  >>> from zope.publisher.browser import TestRequest
  >>> request = TestRequest()
  >>> view = component.getMultiAdapter((manfred, request), name='edit')
  >>> len(view.form_fields)
  2
  >>> [w.__name__ for w in view.form_fields]
  ['name', 'size']
"""
import grok
from zope import schema

class Mammoth(grok.Model):
    class fields:
        name = schema.TextLine(title=u"Name")
        size = schema.TextLine(title=u"Size", default=u"Quite normal")
        somethingelse = None

class Edit(grok.EditForm):
    pass
