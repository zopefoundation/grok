"""
Multiple models lead to ambiguity:

  >>> grok.grok(__name__)
  Traceback (most recent call last):
    ...
  GrokError: Multiple possible contexts for
  <class 'grok.tests.adapter.multiple.Home'>, please use grok.context.

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
