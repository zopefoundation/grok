"""
  >>> grok.testing.grok(__name__)

  >>> cave = Cave()
  >>> home = IHome(cave)

  >>> IHome.providedBy(home)
  True
  >>> isinstance(home, Home)
  True

  >>> fireplace = IFireplace(cave)
  >>> IFireplace.providedBy(fireplace)
  True
  >>> isinstance(fireplace, Fireplace)
  True
"""

import grok
from zope import interface

class Cave(grok.Model):
    pass

class IHome(interface.Interface):
    pass

class Home(grok.Adapter):
    grok.implements(IHome)

class IFireplace(interface.Interface):
    pass

class Fireplace(grok.Adapter):
    grok.implements(IFireplace, IHome)
    grok.provides(IFireplace)
