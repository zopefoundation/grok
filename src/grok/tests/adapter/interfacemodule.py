"""
You can also specify interfaces instead of classes with
`grok.context` (module-level):

  >>> grok.testing.grok(__name__)

  >>> cave = Cave()
  >>> home = IHome(cave)

  >>> IHome.providedBy(home)
  True
  >>> isinstance(home, Home)
  True

  >>> hole = Hole()
  >>> home = IHome(hole)

  >>> IHome.providedBy(home)
  True
  >>> isinstance(home, Home)
  True

"""
from zope import interface

import grok


class ICave(interface.Interface):
    pass


@grok.implementer(ICave)
class Cave(grok.Model):
    pass


@grok.implementer(ICave)
class Hole(grok.Model):
    pass


grok.context(ICave)


class IHome(interface.Interface):
    pass


@grok.implementer(IHome)
class Home(grok.Adapter):
    pass
