"""
TemplateFactories allow use to define page templates in python code.

  >>> import grok
  >>> from mars.template.tests.template import Mammoth
  >>> grok.grok('mars.template.tests.template')

  >>> mammoth = Mammoth()
  >>> import zope.component
  >>> from zope.pagetemplate.interfaces import IPageTemplate
  >>> from zope.publisher.browser import TestRequest
  >>> request = TestRequest()
  >>> from mars.template.tests.template import View
  >>> view = View(mammoth, request)

The template can then be looked up for the object that it is registered for
using grok.context.

  >>> template = zope.component.getMultiAdapter(
  ...              (view, request), IPageTemplate)
  >>> print template
  <zope.app.pagetemplate.viewpagetemplatefile.ViewPageTemplateFile object at ...>

  >>> print view.render()
  <div>View template</div>

TemplateFactories support a `macro` directive (see z3c.template).

  >>> from mars.template.tests.template import Macro
  >>> macro = Macro(mammoth, request)
  >>> print macro.render()
  <div>This is within the mymacro macro</div>

TemplateFactories also allow the setting of the contentType.

  >>> from mars.template.tests.template import PlainText
  >>> plaintext = PlainText(mammoth, request)
  >>> template = zope.component.getMultiAdapter(
  ...              (plaintext, request), IPageTemplate)
  >>> print template.content_type
  text/plain

"""

import zope.component
from zope.pagetemplate.interfaces import IPageTemplate

import grok

import mars.template

class Mammoth(grok.Model):
    pass

class TemplateView(grok.View):

    def render(self):
        template = zope.component.getMultiAdapter(
            (self, self.request), IPageTemplate)
        return template(self)

class View(TemplateView):
    pass

class ViewTemplate(mars.template.TemplateFactory):
    grok.template('templates/view.pt')
    grok.context(View) # this is template for View 

class Macro(TemplateView):
    pass

class MacroTemplate(mars.template.TemplateFactory):
    grok.template('templates/macro.pt')
    grok.context(Macro)
    mars.template.macro('mymacro')

class PlainText(TemplateView):
    pass

class PlainTextTemplate(mars.template.TemplateFactory):
    grok.template('templates/plain.pt')
    grok.context(PlainText)
    mars.template.content_type('text/plain')



