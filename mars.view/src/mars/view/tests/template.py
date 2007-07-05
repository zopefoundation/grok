"""
Testing the TemplateView, which unlike grok.View will look up a template.

  >>> import grok
  >>> from mars.view.tests.template import Mammoth, Painting
  >>> grok.grok('mars.view.tests.template')
  >>> mammoth = getRootFolder()["manfred"] = Mammoth()

  >>> from zope.testbrowser.testing import Browser
  >>> browser = Browser()
  >>> browser.handleErrors = False

TemplateViews look up a template as an adpater.

  >>> from zope.publisher.browser import TestRequest
  >>> request = TestRequest()
  >>> view = Painting(mammoth, request)
  >>> from zope.publisher.interfaces.browser import IBrowserView

Since a template is not yet registered, rendering the view will fail:

  >>> print view.render()
  Traceback (most recent call last):
  ...
  ComponentLookupError: ......

We can register a template for the view.

  >>> import os, tempfile
  >>> temp_dir = tempfile.mkdtemp()
  >>> from zope.pagetemplate.interfaces import IPageTemplate
  >>> from z3c.template.template import TemplateFactory
  >>> from zope.publisher.interfaces.browser import IBrowserRequest
  >>> import zope.component
  >>> template = os.path.join(temp_dir, 'template.pt')
  >>> open(template, 'w').write('''
  ...   <div>Rendered content</div>
  ... ''')

  >>> factory = TemplateFactory(template, 'text/html')
  >>> zope.component.provideAdapter(factory,
  ...     (Painting, IBrowserRequest), IPageTemplate)

  >>> print view.render()
  <div>Rendered content</div>

  >>> import shutil
  >>> shutil.rmtree(temp_dir)

We can also use mars.template to provide the template.

  >>> from mars.view.tests.template import View
  >>> view = View(mammoth, request)
  >>> print view.render()
  <div>View template</div>

"""
import grok
import mars.view
import mars.template

class Mammoth(grok.Model):
    pass

class Painting(mars.view.TemplateView):
    pass

class View(mars.view.TemplateView):
    pass

class ViewTemplate(mars.template.TemplateFactory):
    grok.template('templates/template.pt')
    grok.context(View)


