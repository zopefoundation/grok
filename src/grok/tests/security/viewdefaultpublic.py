"""
Views are public by default:

  >>> grok.grok(__name__)

  >>> manfred = Mammoth()

  >>> from zope.security.management import newInteraction, endInteraction
  >>> newInteraction()

  >>> from zope.publisher.browser import TestRequest
  >>> request = TestRequest()
  >>> from zope import component
  >>> view = component.getMultiAdapter((manfred, request), name='cavepainting')

  >>> from zope.security.proxy import ProxyFactory
  >>> view = ProxyFactory(view)
  >>> print view()
  A cave painting of a mammoth

Same goes for template-based views:

  >>> view = component.getMultiAdapter((manfred, request), name='templatepainting')
  >>> view = ProxyFactory(view)
  >>> print view()
  A template-based painting of a mammoth

  >>> endInteraction()

"""
import grok

class Mammoth(grok.Model):
    pass

class CavePainting(grok.View):

    def render(self):
        return 'A cave painting of a mammoth'

templatepainting = grok.PageTemplate("""\
A template-based painting of a mammoth
""")
