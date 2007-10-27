"""
Before a view is rendered, the update() method is executed. It can be
used e. g. to execute side effects or set up data for use in the
template.

  >>> grok.testing.grok(__name__)

We need to set up a default ITraversable adapter so that TALES
expressions can resolve paths:

  >>> from zope import component
  >>> from zope.traversing.adapters import DefaultTraversable
  >>> component.provideAdapter(DefaultTraversable, (None,))

  >>> manfred = Mammoth()
  >>> from zope.publisher.browser import TestRequest
  >>> request = TestRequest()
  >>> view = component.getMultiAdapter((manfred, request), name='cavepainting')
  >>> print view()
  <html>
  <body>
  <h1>red</h1>
  <h1>red</h1>
  </body>
  </html>
  

"""
import grok

class Mammoth(grok.Model):
    pass

class CavePainting(grok.View):
    def update(self):
        self.color = "red"


cavepainting = grok.PageTemplate("""\
<html>
<body>
<h1 tal:content="view/color"/>
<h1 tal:content="python: view.color"/>
</body>
</html>
""")
