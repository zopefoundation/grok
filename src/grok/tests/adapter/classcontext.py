"""
Explicit class-level context in case of multiple models:

  >>> grok.testing.grok(__name__)

  >>> cave = Cave()
  >>> home = IHome(cave)

  >>> IHome.providedBy(home)
  True
  >>> isinstance(home, Home)
  True

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
    grok.context(Cave)
