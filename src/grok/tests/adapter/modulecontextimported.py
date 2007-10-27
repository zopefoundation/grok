"""
Explicit module-level context for an imported model:

  >>> grok.testing.grok(__name__)

  >>> cave = Cave()
  >>> painting = IPainting(cave)

  >>> IPainting.providedBy(painting)
  True
  >>> isinstance(painting, Painting)
  True

"""
import grok
from grok.tests.adapter.adapter import Cave
from zope import interface

grok.context(Cave)

class IPainting(interface.Interface):
    pass

class Painting(grok.Adapter):
    grok.implements(IPainting)
