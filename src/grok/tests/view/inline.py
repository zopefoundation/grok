"""
Templates can be specified in the same module as the view,
using a variable named `viewname_pt`:

  >>> grok.grok(__name__)
  
  >>> manfred = Mammoth()
  >>> from zope.publisher.browser import TestRequest
  >>> request = TestRequest()
  >>> from zope import component
  >>> view = component.getMultiAdapter((manfred, request), name='cavepainting')
  >>> print view()
  <html>
  <body><h1>Mammoth Cave Painting</h1></body>
  </html>
"""
import grok

class Mammoth(grok.Model):
    pass

class CavePainting(grok.View):
    pass

cavepainting_pt = """\
<html>
<body><h1 tal:content="string:Mammoth Cave Painting"/></body>
</html>
"""
