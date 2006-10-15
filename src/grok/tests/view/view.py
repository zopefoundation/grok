"""

  >>> grok.grok(__name__)

  >>> manfred = Mammoth()
  >>> from zope.publisher.browser import TestRequest
  >>> request = TestRequest()
  >>> from zope import component
  >>> view = component.getMultiAdapter((manfred, request), name='cavepainting')
  >>> view()
  'A cave painting of a mammoth'

"""

import grok

class Mammoth(grok.Model):
    pass

class CavePainting(grok.View):

    def render(self):
        return 'A cave painting of a mammoth'
