"""
Multiple models lead to ambiguity:

  >>> grok.testing.grok(__name__)
  Traceback (most recent call last):
    ...
  GrokError: Multiple possible contexts for
  <class 'grok.tests.adapter.multiple.Home'>, please use the
  'context' directive.

"""
import grok
from zope import interface

class Cave(grok.Model):
    pass

class Club(grok.Model):
    pass

class IHome(interface.Interface):
    pass

class Home(grok.Adapter):
    grok.implements(IHome)
