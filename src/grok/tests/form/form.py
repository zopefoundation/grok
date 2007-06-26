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

If the 'fields' attribute is not an old-style class, it will not trigger any
attribute generation:

  >>> cave = Cave()
  >>> cave.ignored
  Traceback (most recent call last):
    ...
  AttributeError: 'Cave' object has no attribute 'ignored'

A grok.EditForm is a special grok.View that renders an edit form.

  >>> from zope import component
  >>> from zope.publisher.browser import TestRequest
  >>> request = TestRequest()
  >>> view = component.getMultiAdapter((manfred, request), name='edit')
  >>> len(view.form_fields)
  2
  >>> [w.__name__ for w in view.form_fields]
  ['name', 'size']

It is important to keep the order of the fields:

  >>> view = component.getMultiAdapter(
  ...    (DifferentMammoth(), request), name='editdifferent')
  >>> len(view.form_fields)
  2
  >>> [w.__name__ for w in view.form_fields]
  ['size', 'name']

"""
import grok
from zope import schema

class Mammoth(grok.Model):
    class fields:
        name = schema.TextLine(title=u"Name")
        size = schema.TextLine(title=u"Size", default=u"Quite normal")
        somethingelse = None

class Edit(grok.EditForm):
    grok.context(Mammoth)

class Cave(grok.Model):
    fields = ['ignored']

class DifferentMammoth(grok.Model):
    class fields:
        # mind the different order of fields
        size = schema.TextLine(title=u"Size", default=u"Quite normal")
        name = schema.TextLine(title=u"Name")

class EditDifferent(grok.EditForm):
    grok.context(DifferentMammoth)
