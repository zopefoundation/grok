"""
Explicit module-level context in case of multiple models:

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

grok.context(Cave)

class IHome(interface.Interface):
    pass

@grok.implementer(IHome)
class Home(grok.Adapter):
    pass
