"""
LayoutFactories allow use to define page templates in python code.

  >>> import grok
  >>> from mars.template.tests.layout import Mammoth
  >>> grok.grok('mars.template.tests.layout')

  >>> mammoth = getRootFolder()["mammoth"] = Mammoth()

Layout views have a call method (TemplateViews do not necessarily) so we will
use testbrowser.

  >>> from zope.testbrowser.testing import Browser
  >>> browser = Browser()
  >>> browser.handleErrors = False

  >>> browser.open("http://localhost/mammoth/@@view")
  >>> print browser.contents
  <div>View template</div>

Like TemplateFactories, LayoutFactories also support a `macro` directive (see z3c.template).

  >>> browser.open("http://localhost/mammoth/@@macro")
  >>> print browser.contents
  <div>This is within the mymacro macro</div>

And also allow the setting of the contentType. But I haven't got that to render yet.

  >>> import zope.component
  >>> from z3c.template.interfaces import ILayoutTemplate
  >>> from mars.template.tests.layout import PlainText
  >>> from zope.publisher.browser import TestRequest
  >>> request = TestRequest()
  >>> plaintext = PlainText(mammoth, request)
  >>> template = zope.component.getMultiAdapter(
  ...              (plaintext, request), ILayoutTemplate)
  >>> print template.content_type
  text/plain

"""

import zope.component

from z3c.template.interfaces import ILayoutTemplate

import grok

import mars.template

class Mammoth(grok.Model):
    pass

class LayoutView(grok.View):

    def __call__(self):
        template = zope.component.getMultiAdapter(
            (self, self.request), ILayoutTemplate)
        return template(self)

    def render(self):
        pass

class View(LayoutView):
    pass

class ViewLayout(mars.template.LayoutFactory):
    grok.template('templates/view.pt')
    grok.context(View) # this is template for View 

class Macro(LayoutView):
    pass

class MacroLayout(mars.template.LayoutFactory):
    grok.template('templates/macro.pt')
    grok.context(Macro)
    mars.template.macro('mymacro')

class PlainText(LayoutView):
    pass

class PlainTextLayout(mars.template.LayoutFactory):
    grok.template('templates/plain.pt')
    grok.context(PlainText)
    mars.template.content_type('text/plain')





