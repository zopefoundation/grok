"""
Subclasses of grok.Adapter and grok.MultiAdapter must implement exactly one
interface:

  >>> grok.testing.grok(__name__)
  Traceback (most recent call last):
    ...
  GrokError: <class 'grok.tests.adapter.implementsmany.Home'> is implementing
  more than one interface (use grok.provides to specify which one to use).
"""
import grok

from zope import interface

class Cave(grok.Model):
    pass

class IHome(interface.Interface):
    pass

class IFireplace(interface.Interface):
    pass

class Home(grok.Adapter):
    grok.implements(IHome, IFireplace)
