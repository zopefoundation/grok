"""
  >>> import grok
  >>> from megrok.template.tests.template.layoutview import Mammoth
  >>> grok.grok('megrok.template.tests.template.layoutview')

  >>> mammoth = getRootFolder()["mammoth"] = Mammoth()

Layout views have a call method (TemplateViews do not) so we can use testbrowser.

  >>> from zope.testbrowser.testing import Browser
  >>> browser = Browser()
  >>> browser.handleErrors = False

  >>> browser.open("http://localhost/mammoth/@@painting")
  >>> print browser.contents
  <div>Mammoth view</div>

Like TemplateFactories, LayoutFactories also support a `macro` directive (see z3c.template).

  >>> browser.open("http://localhost/mammoth/@@drawing")
  >>> print browser.contents
  <div>This is within the mymacro macro</div>

And also allow the setting of the contentType. But I haven't got that to render yet.

  >>> import zope.component
  >>> from z3c.template.interfaces import ILayoutTemplate
  >>> from megrok.template.tests.template.layoutview import TextDrawing
  >>> from zope.publisher.browser import TestRequest
  >>> request = TestRequest()
  >>> plaintext = TextDrawing(mammoth, request)
  >>> template = zope.component.getMultiAdapter(
  ...              (plaintext, request), ILayoutTemplate)
  >>> print template.content_type
  text/plain

"""

import grok

import megrok.template
import megrok.view

class Mammoth(grok.Model):
    pass

class Painting(megrok.view.LayoutView):
    pass

    def render(self):
        return u'Mammoth view'

class LayoutTemplate(megrok.template.LayoutFactory):
    """Only file templates can be used with template factory"""
    grok.context(Painting) # this is layout template for Painting

class Drawing(megrok.view.LayoutView):
    pass

class DrawingTemplate(megrok.template.LayoutFactory):
    """Only file templates can be used with template factory"""
    grok.context(Drawing)
    megrok.template.macro('mymacro')

class TextDrawing(megrok.view.LayoutView):
    pass

    def render(self):
        return self.response.getHeader('Content-Type')

class TextDrawingTemplate(megrok.template.LayoutFactory):
    """Only file templates can be used with template factory"""
    grok.context(TextDrawing)
    megrok.template.content_type('text/plain')

