"""
Subclasses of grok.MultiAdapter must declare what they adapt, using grok.adapts:

  >>> grok.testing.grok(__name__)
  Traceback (most recent call last):
    ...
  GrokError: <class 'grok.tests.adapter.multiadaptsnone.Home'> must specify
  which contexts it adapts (use the 'adapts' directive to specify).
"""
import grok

from zope import interface

class IHome(interface.Interface):
    pass

class Home(grok.MultiAdapter):
    grok.implements(IHome)
