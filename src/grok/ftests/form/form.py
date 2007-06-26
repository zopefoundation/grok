"""
A grok.EditForm is a special grok.View that renders an edit form.

  >>> import grok
  >>> from grok.ftests.form.form import Mammoth
  >>> grok.grok('grok.ftests.form.form')
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

class Mammoth(grok.Model):
    class fields:
        name = schema.TextLine(title=u"Name")
        size = schema.TextLine(title=u"Size")

class Edit(grok.EditForm):
    pass

class Display(grok.DisplayForm):
    pass

