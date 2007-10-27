"""
A grok.Fields can receive keyword parameters with schema fields. These
should be avaible in the definition order.

  >>> grok.testing.grok(__name__)

  >>> from zope import component
  >>> from zope.publisher.browser import TestRequest
  >>> request = TestRequest()
  >>> view = component.getMultiAdapter((Mammoth(), request), name='edit')
  >>> len(view.form_fields)
  4
  >>> [w.__name__ for w in view.form_fields]
  ['a', 'b', 'g', 'd']

"""
import grok
from zope import schema

class Mammoth(grok.Model):
    pass

class Edit(grok.EditForm):
    form_fields = grok.Fields(
        a = schema.TextLine(title=u"Alpha"),
        b = schema.TextLine(title=u"Beta"),
        g = schema.TextLine(title=u"Gamma"),
        d = schema.TextLine(title=u"Delta"))
    
