"""
Anything can be registered as a local utility. If it implements a single
interface, there is no need to specify which interface it provides.

In this test, the utility does not implement any interface, so it cannot be
registered as a local utility.

  >>> grok.grok(__name__)
  Traceback (most recent call last):
    ...
  GrokError: <class 'grok.tests.utility.local_implementsnone.Fireplace'>
  must implement at least one interface (use grok.implements to specify).

"""

import grok
from zope import interface

class Fireplace(object):
    pass

class Cave(grok.Model, grok.Site):
    grok.local_utility(Fireplace)
