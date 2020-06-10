"""
Old-style classes are also supported:

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


class Cave:
    pass


class IHome(interface.Interface):
    pass


@grok.implementer(IHome)
class Home(grok.Adapter):
    grok.context(Cave)
