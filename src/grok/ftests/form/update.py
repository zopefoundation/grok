"""
Forms can implement an update() method that will be called before any
form processing has happened:

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

A form's update() method can issue a redirect.  In that case, the form
won't proceed to do any form processing nor rendering:

  >>> browser.open("http://localhost/manfred/editredirect")
  >>> browser.getControl(name="form.name").value = "Mallie"
  >>> browser.getControl("Apply").click()
  >>> print browser.url
  http://localhost/manfred/index

Because of the redirect, no changes happened to the edited object:

  >>> print browser.contents
  Ellie, the Mammoth reports: The form's update() was called and my name was Manfred.

A form's update() method may also take arbitrary parameters that will
be filled with values from the request (such as form values):

  >>> browser.open("http://localhost/manfred/editupdatewitharguments")
  >>> browser.getControl(name="report").value = "Request argument dispatch to update() works."
  >>> browser.getControl(name="form.name").value = "Mallie"
  >>> browser.getControl("Apply").click()

  >>> browser.open("http://localhost/manfred")
  >>> print browser.contents
  Mallie, the Mammoth reports: Request argument dispatch to update() works.

"""
import grok
from zope import schema

from zope.interface import Interface, implements

class IMammoth(Interface):
    name = schema.TextLine(title=u"Name")

class Mammoth(grok.Model):
    implements(IMammoth)
    
    name = u'Manfred'

class Index(grok.View):

    def render(self):
        return "%s, the Mammoth reports: %s" % (self.context.name,
                                                self.context.report)

class Edit(grok.EditForm):

    def update(self):
        self.context.report = ("The form's update() was called and my name "
                               "was %s." % self.context.name)

class EditRedirect(grok.EditForm):

    def update(self):
        # redirect upon form submit so that no changes are ever saved
        if 'form.name' in self.request:
            self.redirect(self.url('index'))

class EditUpdateWithArguments(grok.EditForm):

    def update(self, report=None):
        if report is not None:
            self.context.report = report

editupdatewitharguments = grok.PageTemplate("""
<html>
<body>
<form action="" tal:attributes="action request/URL">
  <input type="text" name="report" />
  <div tal:repeat="widget view/widgets" tal:content="structure widget" />
  <div tal:repeat="action view/actions" tal:content="structure action/render" />
</form>
</body>
</html>
""")
