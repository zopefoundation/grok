"""
Templates can also be found in a directory with the same name as the module:

  >>> grok.testing.grok(__name__)
  
  >>> manfred = Mammoth()
  >>> from zope.publisher.browser import TestRequest
  >>> request = TestRequest()
  >>> from zope import component
  >>> view = component.getMultiAdapter((manfred, request), name='cavepainting')
  >>> print view()
  <html>
  <body>
  A cave painting.
  </body>
  </html>

  >>> view = component.getMultiAdapter((manfred, request), name='food')
  >>> print view()
  <html>
  <body>
  ME GROK EAT MAMMOTH!
  </body>
  </html>

"""
import grok

class Mammoth(grok.Model):
    pass

class CavePainting(grok.View):
    pass

class Food(grok.View):
    pass
