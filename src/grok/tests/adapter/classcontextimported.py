"""
Explicit class-level context for an imported model:

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


class IPainting(interface.Interface):
    pass


@grok.implementer(IPainting)
class Painting(grok.Adapter):
    grok.context(Cave)
