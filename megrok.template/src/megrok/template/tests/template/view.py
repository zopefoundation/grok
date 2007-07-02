"""
  >>> import grok
  >>> from megrok.template.tests.template.view import MyFactory, Mammoth
  >>> grok.grok('megrok.template.tests.template.view')

  >>> mammoth = Mammoth()
  >>> import zope.component
  >>> from zope.pagetemplate.interfaces import IPageTemplate
  >>> from zope.publisher.browser import TestRequest
  >>> request = TestRequest()
  >>> template = zope.component.getMultiAdapter(
  ...              (mammoth, request), IPageTemplate)
  >>> print template
  <zope.app.pagetemplate.viewpagetemplatefile.ViewPageTemplateFile object at ...>

"""

import grok

import megrok.template
import zope.interface

class Mammoth(grok.Model):
    pass

class MyFactory(megrok.template.TemplateFactory):
    pass

#myfactory = grok.PageTemplate("""\
#<div>Factory template</div>
#""")

