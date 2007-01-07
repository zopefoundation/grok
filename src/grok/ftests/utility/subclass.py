"""
Subclassed sites inherit all local utilities of their base classes:

  >>> import grok
  >>> from zope import component
  >>> from grok.ftests.utility.subclass import *

  >>> grok.grok('grok.ftests.utility.subclass')

  >>> cave = BigCave()
  >>> getRootFolder()["cave"] = cave

  >>> from zope.app.component.hooks import getSite, setSite

  >>> setSite(cave)
  >>> fireplace = component.getUtility(IFireplace)
  >>> IFireplace.providedBy(fireplace)
  True
  >>> isinstance(fireplace, Fireplace)
  True

Additional utilities can be registered in the subclass:
  
  >>> hollow = HollowCave()
  >>> getRootFolder()["hollow"] = hollow

  >>> setSite(hollow)
  >>> fireplace = component.getUtility(IFireplace)
  >>> IFireplace.providedBy(fireplace)
  True
  >>> isinstance(fireplace, Fireplace)
  True

  >>> painting = component.getUtility(IPainting)
  >>> IPainting.providedBy(painting)
  True
  >>> isinstance(painting, Painting)
  True

Those do not influence the base class:

  >>> setSite(cave)
  >>> painting = component.getUtility(IPainting)
  Traceback (most recent call last):
    ...
  ComponentLookupError: (<InterfaceClass grok.ftests.utility.subclass.IPainting>, '')
"""
import grok
from zope import interface

class IFireplace(interface.Interface):
    pass

class IPainting(interface.Interface):
    pass

class Fireplace(grok.LocalUtility):
    grok.implements(IFireplace)

class Painting(grok.LocalUtility):
    grok.implements(IPainting)

class Cave(grok.Model, grok.Site):
    # we use name_in_container here to prevent multiple registrations
    # since storing the utilities multiple times under the same name
    # would raise a DuplicationError
    grok.local_utility(Fireplace, name_in_container='fireplace')

class BigCave(Cave):
    pass

class HollowCave(Cave):
    grok.local_utility(Painting)
