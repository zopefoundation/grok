"""
Testing the LayoutView, which unlike grok.View will look up a layout.

  >>> import grok
  >>> grok.grok('mars.view.tests.layout')
  >>> from mars.view.tests.layout import Mammoth
  >>> getRootFolder()["manfred"] = Mammoth()

  >>> from zope.testbrowser.testing import Browser
  >>> browser = Browser()
  >>> browser.handleErrors = False

These tests make use of minimal layer

  >>> skinURL = 'http://localhost/++skin++myskin'

Since a layout template is not yet registered, calling the view will fail:

  >>> browser.open("http://localhost/manfred/@@drawing")
  Traceback (most recent call last):
  ...
  NotFound: ......

  >>> browser.open(skinURL + "/manfred/@@drawing")
  Traceback (most recent call last):
  ...
  ComponentLookupError: ......

We'll manually register a layout template.

  >>> import os, tempfile
  >>> temp_dir = tempfile.mkdtemp()
  >>> layout = os.path.join(temp_dir, 'layout.pt')
  >>> open(layout, 'w').write('''
  ...   <div tal:content="view/render">
  ...     Full layout
  ...   </div>
  ... ''')

  >>> from z3c.template.interfaces import ILayoutTemplate
  >>> from z3c.template.template import TemplateFactory
  >>> from zope.publisher.interfaces.browser import IBrowserRequest
  >>> import zope.component
  >>> from mars.view.tests.layout import Drawing
  >>> factory = TemplateFactory(layout, 'text/html')
  >>> zope.component.provideAdapter(factory,
  ...     (Drawing, IBrowserRequest), ILayoutTemplate)

  >>> browser.open(skinURL + "/manfred/@@drawing")
  >>> print browser.contents
  <div>Rendered content</div>

  >>> import shutil
  >>> shutil.rmtree(temp_dir)

We can also use mars.template to provide the layout template.

  >>> browser.open(skinURL + "/manfred/@@view")
  >>> print browser.contents
  <div>View template</div>

Both layout and template can be used with LayoutView, the template being
rendered by LayoutView's `render` method.

  >>> browser.open(skinURL + "/manfred/@@full")
  >>> print browser.contents
  <html>
  <body><div>View template</div>
  </body>
  </html>
  <BLANKLINE>


"""
import zope.interface

import grok
import mars.view
import mars.template
import mars.layer

class IMyLayer(mars.layer.IMinimalLayer):
    pass

# set layer on module level, all class declarations that use directive
# mars.layer.layer will use this layer - Skin, views and templates
mars.layer.layer(IMyLayer)

class MySkin(mars.layer.Skin):
    pass

class Mammoth(grok.Model):
    pass

class Drawing(mars.view.LayoutView):
    pass

    def render(self):
        return u'Rendered content'

class View(mars.view.LayoutView):
    pass

class ViewLayout(mars.template.LayoutFactory):
    grok.template('templates/template.pt')
    grok.context(View)

class Full(mars.view.LayoutView):
    pass

class FullLayout(mars.template.LayoutFactory):
    grok.template('templates/layout.pt')
    grok.context(Full)

class FullTemplate(mars.template.TemplateFactory):
    grok.template('templates/template.pt')
    grok.context(Full)

