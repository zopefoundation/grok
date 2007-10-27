"""
Anything can be registered as a local utility. If it implements a single
interface, there is no need to specify which interface it provides.

In this test, the utility implements more than one interface, so it cannot be
registered as a local utility.

  >>> grok.testing.grok(__name__)
  Traceback (most recent call last):
    ...
  GrokError: <class 'grok.tests.utility.local_implementsmany.Fireplace'>
  is implementing more than one interface (use grok.provides to specify
  which one to use).

"""

import grok
from zope import interface

class IHome(interface.Interface):
    pass

class IFireplace(interface.Interface):
    pass

class Fireplace(object):
    interface.implements(IHome, IFireplace)

class Cave(grok.Model, grok.Site):
    grok.local_utility(Fireplace)
