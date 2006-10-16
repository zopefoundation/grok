"""
Before a view is rendered, the before() method is executed. It can be
used e. g. to execute side effects or set up data for use in the
template.

  >>> grok.grok(__name__)

  >>> manfred = Mammoth()
  >>> from zope.publisher.browser import TestRequest
  >>> request = TestRequest()
  >>> from zope import component
  >>> view = component.getMultiAdapter((manfred, request), name='cavepainting')
  >>> print view()
  <html>
  <body>
  <h1>red</h1>
  </body>
  </html>
  

"""
import grok

class Mammoth(grok.Model):
    pass

class CavePainting(grok.View):
    def before(self):
        self.color = "red"


cavepainting = grok.PageTemplate("""\
<html>
<body>
<h1 tal:content="python: view.color"/>
</body>
</html>
""")
