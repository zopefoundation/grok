"""
A grok.EditForm is a special grok.View that renders an edit form.

  >>> from zope import component
  >>> from zope.publisher.browser import TestRequest
  >>> grok.grok(__name__)
  >>> manfred = Mammoth()

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
from zope.interface import Interface, implements

class IMammoth(Interface):
    name = schema.TextLine(title=u"Name")
    size = schema.TextLine(title=u"Size", default=u"Quite normal")

class Mammoth(grok.Model):
    implements(IMammoth)

class Edit(grok.EditForm):
    grok.context(Mammoth)

class IDifferentMammoth(Interface):
    # mind the different order of fields
    size = schema.TextLine(title=u"Size", default=u"Quite normal")
    name = schema.TextLine(title=u"Name")

class DifferentMammoth(grok.Model):
    implements(IDifferentMammoth)

class EditDifferent(grok.EditForm):
    grok.context(DifferentMammoth)

