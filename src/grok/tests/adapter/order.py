"""
If the model is defined after the adapter, it should still be grokked
properly:

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

class IHome(interface.Interface):
    pass

class Home(grok.Adapter):
    grok.implements(IHome)

class Cave(grok.Model):
    pass
