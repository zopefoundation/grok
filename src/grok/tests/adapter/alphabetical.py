"""
Grok does not depend on the alphabetical order:

  >>> grok.testing.grok(__name__)

  >>> cave = ZCave()
  >>> home = IHome(cave)

  >>> IHome.providedBy(home)
  True
  >>> isinstance(home, Home)
  True

"""
import grok
from zope import interface


class ZCave(grok.Model):
    """we call this `ZCave` because we want to test that we do not
    depend on alphabetical order"""


class IHome(interface.Interface):
    pass


@grok.implementer(IHome)
class Home(grok.Adapter):
    pass
