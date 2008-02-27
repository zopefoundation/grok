"""
You can register a named adapter by using grok.name:

  >>> grok.testing.grok(__name__)

  >>> cave = Cave()
  >>> home = IHome(cave)
  Traceback (most recent call last):
    ...
  TypeError: ('Could not adapt', <grok.tests.adapter.namedadapter.Cave object at 0x...>, <InterfaceClass grok.tests.adapter.namedadapter.IHome>)

  >>> from zope.component import getAdapter
  >>> home = getAdapter(cave, IHome, name='home')
  >>> IHome.providedBy(home)
  True
  >>> isinstance(home, Home)
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
    grok.name('home')
