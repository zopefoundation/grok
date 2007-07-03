"""
Testing the TemplateView, which unlike grok.View will look up a template.

  >>> import grok
  >>> from megrok.view.tests.view.template import Mammoth, Painting
  >>> grok.grok('megrok.view.tests.view.template')
  >>> mammoth = getRootFolder()["manfred"] = Mammoth()

  >>> from zope.testbrowser.testing import Browser
  >>> browser = Browser()
  >>> browser.handleErrors = False

TemplateViews look up a template as an adpater.

  >>> from zope.publisher.browser import TestRequest
  >>> request = TestRequest()
  >>> view = Painting(mammoth, request)

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

TemplateViews support inline templates and file templates
just like any grok view. (But then you may as well use View).

  >>> from megrok.view.tests.view.template import Drawing
  >>> view = Drawing(mammoth, request)
  >>> print view.render()
  <div>Drawing template</div>

  >>> from megrok.view.tests.view.template import Carving
  >>> view = Carving(mammoth, request)
  >>> print view.render()
  <div>Carving inline template</div>

We can also use megrok.template to provide more sophisticated possiblities.

  >>> from megrok.view.tests.view.template import SculptureView
  >>> view = SculptureView(mammoth, request)
  >>> print view.render()
  <div>Sculpture template</div>

"""
import grok
import megrok.view
import megrok.template

class Mammoth(grok.Model):
    pass

class Painting(megrok.view.TemplateView):
    pass

class Drawing(megrok.view.TemplateView):
    pass

class Carving(megrok.view.TemplateView):
    pass

carving = grok.PageTemplate("""\
<div>Carving inline template</div>
""")

class SculptureView(megrok.view.TemplateView):
    """We don't need to define a template here because the following
    TemplateFactory will be used"""
    pass

class Sculpture(megrok.template.TemplateFactory):
    grok.context(SculptureView)

