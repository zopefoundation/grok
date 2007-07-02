"""
Testing the LayoutView, which unlike grok.View will look up a layout.

  >>> import grok
  >>> from megrok.view.tests.view.layout import Mammoth
  >>> grok.grok('megrok.view.tests.view.layout')
  >>> getRootFolder()["manfred"] = Mammoth()

  >>> from zope.testbrowser.testing import Browser
  >>> browser = Browser()
  >>> browser.handleErrors = False

Since a layout template is not yet registered, calling the view will fail:

  >>> browser.open("http://localhost/manfred/@@painting")
  Traceback (most recent call last):
  ...
  ComponentLookupError: ......

  >>> import os, tempfile
  >>> temp_dir = tempfile.mkdtemp()
  >>> from z3c.template.interfaces import ILayoutTemplate
  >>> from zope.pagetemplate.interfaces import IPageTemplate
  >>> from z3c.template.template import TemplateFactory
  >>> from zope.publisher.interfaces.browser import IBrowserRequest
  >>> import zope.component
  >>> from megrok.view.tests.view.layout import Painting
  >>> layout = os.path.join(temp_dir, 'layout.pt')
  >>> open(layout, 'w').write('''
  ...   <div tal:content="view/render">
  ...     Full layout
  ...   </div>
  ... ''')

  >>> factory = TemplateFactory(layout, 'text/html')
  >>> zope.component.provideAdapter(factory,
  ...     (Painting, IBrowserRequest), ILayoutTemplate)

  >>> browser.open("http://localhost/manfred/@@painting")
  >>> print browser.contents
  <div>Rendered content</div>

Cleanup
-------

  >>> import shutil
  >>> shutil.rmtree(temp_dir)

"""

import grok
import megrok.view

class Mammoth(grok.Model):
    pass

class Painting(megrok.view.LayoutView):
    pass

    def render(self):
        return u'Rendered content'
