"""
If a form does not have a template, a simple default template is
associated with them. Otherwise, the supplied template is used.

  >>> from zope.publisher.browser import TestRequest
  >>> request = TestRequest()
  >>> from zope import component
  
Default edit template:

  >>> view = component.getMultiAdapter((Mammoth(), request), name='edit')
  >>> print view()
  <html>...
  
Custom edit template:

  >>> view = component.getMultiAdapter((Mammoth(), request), name='edit2')
  >>> print view()
  <p>Test edit</p>

Custom edit template with an explicit template

  >>> view = component.getMultiAdapter((Mammoth(), request), name='edit3')
  >>> print view()
  <p>Test edit</p>

Default display template:

  >>> view = component.getMultiAdapter((Mammoth(), request), name='display')
  >>> print view()
  <html>...
  
Custom display template:

  >>> view = component.getMultiAdapter((Mammoth(), request), name='display2')
  >>> print view()
  <p>Test display</p>

Custom display template with an explicit template:

  >>> view = component.getMultiAdapter((Mammoth(), request), name='display3')
  >>> print view()
  <p>Test display</p>

"""
import grok
from zope import schema

class Mammoth(grok.Model):
    class fields:
        name = schema.TextLine(title=u"Name")
        size = schema.TextLine(title=u"Size", default=u"Quite normal")

class Edit(grok.EditForm):
    pass

class Edit2(grok.EditForm):
    pass

edit2 = grok.PageTemplate('<p>Test edit</p>')

class Edit3(grok.EditForm):
    grok.template('edit2')

class Display(grok.DisplayForm):
    pass

class Display2(grok.DisplayForm):
    pass

display2 = grok.PageTemplate('<p>Test display</p>')

class Display3(grok.DisplayForm):
    grok.template('display2')
