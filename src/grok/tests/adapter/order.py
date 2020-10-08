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


@grok.implementer(IHome)
class Home(grok.Adapter):
    pass


class Cave(grok.Model):
    pass
