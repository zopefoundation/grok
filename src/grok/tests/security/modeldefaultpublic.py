"""
Models are public by default:

  >>> grok.grok(__name__)

  >>> mammoth = Mammoth('manfred')

  >>> from zope.security.proxy import ProxyFactory
  >>> from zope.security.management import newInteraction, endInteraction
  >>> mammoth = ProxyFactory(mammoth)
  >>> newInteraction()

  >>> mammoth.name
  'manfred'

  >>> endInteraction()

"""
import grok

class Mammoth(grok.Model):

    def __init__(self, name):
        self.name = name
