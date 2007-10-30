"""
Multi-Adapters are supported by subclassing grok.MultiAdapter, giving
multiple arguments to grok.adapts, and supplying a matching
__init__():

  >>> grok.testing.grok(__name__)

  >>> cave = Cave()
  >>> fireplace = Fireplace()

  >>> from zope import component
  >>> home = component.getMultiAdapter((cave, fireplace))

  >>> IHome.providedBy(home)
  True
  >>> isinstance(home, Home)
  True
  >>> home.cave is cave
  True
  >>> home.fireplace is fireplace
  True

This also works for named adapters using grok.name:

  >>> home = component.getMultiAdapter((cave, fireplace), name='home2')

  >>> IHome.providedBy(home)
  True
  >>> isinstance(home, Home2)
  True
  >>> home.cave is cave
  True
  >>> home.fireplace is fireplace
  True

Multiadapters that implement more than one interface can use grok.provides to
specify the one to use:

  >>> home = component.getMultiAdapter((cave, fireplace), name='home3')

  >>> IHome.providedBy(home)
  True
  >>> isinstance(home, Home3)
  True
  >>> home.cave is cave
  True
  >>> home.fireplace is fireplace
  True
"""

import grok
from zope import interface

class Cave(grok.Model):
    pass

class Fireplace(grok.Model):
    pass

class IHome(interface.Interface):
    pass

class Home(grok.MultiAdapter):
    grok.adapts(Cave, Fireplace)
    grok.implements(IHome)

    def __init__(self, cave, fireplace):
        self.cave = cave
        self.fireplace = fireplace

class Home2(grok.MultiAdapter):
    grok.adapts(Cave, Fireplace)
    grok.implements(IHome)
    grok.name('home2')

    def __init__(self, cave, fireplace):
        self.cave = cave
        self.fireplace = fireplace

class IFireplace(interface.Interface):
    pass

class Home3(grok.MultiAdapter):
    grok.adapts(Cave, Fireplace)
    grok.implements(IHome, IFireplace)
    grok.provides(IHome)
    grok.name('home3')

    def __init__(self, cave, fireplace):
        self.cave = cave
        self.fireplace = fireplace
