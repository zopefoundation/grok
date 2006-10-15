"""

  >>> grok.grok(__name__)

View with an associated PageTemplate that is referred to using
``grok.template``:

  >>> manfred = Mammoth()
  >>> from zope.publisher.browser import TestRequest
  >>> request = TestRequest()
  >>> from zope import component
  >>> view = component.getMultiAdapter((manfred, request), name='painting')
  >>> print view()
  <html><body><h1>GROK PAINT MAMMOTH!</h1></body></html>

"""
import grok

class Mammoth(grok.Model):
    pass

class Painting(grok.View):
    grok.template('cavepainting')

cavepainting = grok.PageTemplate("""\
<html><body><h1>GROK PAINT MAMMOTH!</h1></body></html>
""")
