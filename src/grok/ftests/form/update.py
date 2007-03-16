"""
Forms can implement an update() method that will be called before any
form processing has happened:

  >>> import grok
  >>> grok.grok('grok.ftests.form.update')
  >>> from grok.ftests.form.update import Mammoth
  >>> getRootFolder()["manfred"] = Mammoth()

  >>> from zope.testbrowser.testing import Browser
  >>> browser = Browser()
  >>> browser.handleErrors = False
  >>> browser.open("http://localhost/manfred/edit")
  >>> browser.getControl(name="form.name").value = "Ellie"
  >>> browser.getControl("Apply").click()

  >>> browser.open("http://localhost/manfred")
  >>> print browser.contents
  Ellie, the Mammoth reports: The form's update() was called and my name was Manfred.
"""
import grok
from zope import schema

class Mammoth(grok.Model):
    class fields:
        name = schema.TextLine(title=u"Name", default=u'Manfred')

class Index(grok.View):

    def render(self):
        return "%s, the Mammoth reports: %s" % (self.context.name,
                                                self.context.report)

class Edit(grok.EditForm):

    def update(self):
        self.context.report = ("The form's update() was called and my name "
                               "was %s." % self.context.name)
