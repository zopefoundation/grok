"""
You can explicitly specify the template directory using grok.templatedir on module level:

  >>> grok.grok(__name__)

  >>> manfred = Mammoth()
  >>> from zope.publisher.browser import TestRequest
  >>> request = TestRequest()
  >>> from zope import component
  >>> view = component.getMultiAdapter((manfred, request), name='food')
  >>> print view()
  <html>
  <body>
  ME GROK EAT MAMMOTH!
  </body>
  </html>

"""
import grok

grok.templatedir('templatedirectoryname')

class Mammoth(grok.Model):
    pass

class Food(grok.View):
    pass
