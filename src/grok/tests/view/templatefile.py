"""

  >>> grok.testing.grok(__name__)

View with an associated PageTemplate that is referred to using
``grok.template``:

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
import os.path

class Mammoth(grok.Model):
    pass

class Food(grok.View):
    pass

food = grok.PageTemplate(filename=os.path.join('templatedirectoryname',
                                               'food.pt'))
