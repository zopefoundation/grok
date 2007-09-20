"""
A grok.EditForm is a special grok.View that renders an edit form.

  >>> getRootFolder()["manfred"] = Mammoth()

  >>> from zope.testbrowser.testing import Browser
  >>> browser = Browser()
  >>> browser.handleErrors = False
  >>> browser.open("http://localhost/manfred/@@edit")
  >>> browser.getControl(name="form.name").value = "Manfred the Mammoth"
  >>> browser.getControl(name="form.size").value = "Really big"
  >>> browser.getControl("Apply").click()
  >>> print browser.contents
  <html>...
  ...Manfred the Mammoth...
  ...Really big...
  ...

grok.DisplayForm renders a display form:

  >>> browser.open("http://localhost/manfred/@@display")
  >>> print browser.contents
  <html>...
  ...Manfred the Mammoth...
  ...Really big...
  ...

"""
import grok
from zope import schema
from zope.interface import Interface, implements
from zope.schema.fieldproperty import FieldProperty

class IMammoth(Interface):
    name = schema.TextLine(title=u"Name")
    size = schema.TextLine(title=u"Size", default=u"Quite normal")

class Mammoth(grok.Model):
    implements(IMammoth)
    
    name = FieldProperty(IMammoth['name'])    
    size = FieldProperty(IMammoth['size'])    

class Edit(grok.EditForm):
    pass

class Display(grok.DisplayForm):
    pass

