"""
  >>> import grok
  >>> from megrok.template.tests.template.templateview import Mammoth
  >>> grok.grok('megrok.template.tests.template.templateview')

  >>> mammoth = Mammoth()
  >>> import zope.component
  >>> from zope.pagetemplate.interfaces import IPageTemplate
  >>> from zope.publisher.browser import TestRequest
  >>> request = TestRequest()
  >>> from megrok.template.tests.template.templateview import MammothView
  >>> mammothview = MammothView(mammoth, request)
  >>> template = zope.component.getMultiAdapter(
  ...              (mammothview, request), IPageTemplate)
  >>> print template
  <zope.app.pagetemplate.viewpagetemplatefile.ViewPageTemplateFile object at ...>
  >>> print mammothview.render()
  <div>Factory template</div>

TemplateFactories support a `macro` directive (see z3c.template).

  >>> from megrok.template.tests.template.templateview import MammothViewFromMacro
  >>> mammothviewfrommacro = MammothViewFromMacro(mammoth, request)
  >>> print mammothviewfrommacro.render()
  <div>This is within the mymacro macro</div>

TemplateFactories also allow the setting of the contentType.

  >>> from megrok.template.tests.template.templateview import MammothViewPlainText
  >>> mammothviewplaintext = MammothViewPlainText(mammoth, request)
  >>> template = zope.component.getMultiAdapter(
  ...              (mammothviewplaintext, request), IPageTemplate)
  >>> print template.content_type
  text/plain

"""

import grok

import megrok.template
import megrok.view

class Mammoth(grok.Model):
    pass

class MammothView(megrok.view.TemplateView):
    pass

class MammothViewTemplate(megrok.template.TemplateFactory):
    """Only file templates can be used with template factory"""
    grok.context(MammothView) # this is template for MammothView 

class MammothViewFromMacro(megrok.view.TemplateView):
    pass

class MammothViewFromMacroTemplate(megrok.template.TemplateFactory):
    grok.context(MammothViewFromMacro)
    megrok.template.macro('mymacro')

class MammothViewPlainText(megrok.view.TemplateView):
    pass

class MammothViewPlainTextTemplate(megrok.template.TemplateFactory):
    grok.context(MammothViewPlainText)
    megrok.template.content_type('text/plain')


