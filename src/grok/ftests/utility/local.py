"""
Local Utilities can be registered on subclasses of grok.Site using
grok.local_utility:

  >>> cave = Cave()
  >>> getRootFolder()["cave"] = cave

  >>> from zope import component
  >>> from zope.app.component.hooks import getSite, setSite
  >>> setSite(cave)

  >>> fireplace = component.getUtility(IFireplace)
  >>> IFireplace.providedBy(fireplace)
  True
  >>> isinstance(fireplace, Fireplace)
  True

  >>> club = component.getUtility(IClub)
  >>> IClub.providedBy(club)
  True
  >>> isinstance(club, Club)
  True

  >>> spiky = component.getUtility(IClub, name='spiky')
  >>> IClub.providedBy(spiky)
  True
  >>> isinstance(spiky, SpikyClub)
  True

  >>> mammoth = component.getUtility(IMammoth)
  >>> IMammoth.providedBy(mammoth)
  True
  >>> isinstance(mammoth, Mammoth)
  True

  >>> tiger = component.getUtility(IMammoth, name='tiger')
  >>> IMammoth.providedBy(tiger)
  True
  >>> isinstance(tiger, SabretoothTiger)
  True

  >>> painting = component.getUtility(IPainting, name='blackandwhite')
  >>> IPainting.providedBy(painting)
  True
  >>> isinstance(painting, CavePainting)
  True

  >>> colored = component.getUtility(IPainting, name='color')
  >>> IPainting.providedBy(colored)
  True
  >>> isinstance(colored, ColoredCavePainting)
  True

Since it is a local utility, it is not available outside its site:

  >>> setSite(None)
  >>> component.getUtility(IFireplace)
  Traceback (most recent call last):
    ...
  ComponentLookupError: (<InterfaceClass grok.ftests.utility.local.IFireplace>, '')

  >>> component.getUtility(IClub)
  Traceback (most recent call last):
    ...
  ComponentLookupError: (<InterfaceClass grok.ftests.utility.local.IClub>, '')

  >>> component.getUtility(IClub, name='spiky')
  Traceback (most recent call last):
    ...
  ComponentLookupError: (<InterfaceClass grok.ftests.utility.local.IClub>, 'spiky')

  >>> component.getUtility(IMammoth)
  Traceback (most recent call last):
    ...
  ComponentLookupError: (<InterfaceClass grok.ftests.utility.local.IMammoth>, '')

  >>> component.getUtility(IMammoth, name='tiger')
  Traceback (most recent call last):
    ...
  ComponentLookupError: (<InterfaceClass grok.ftests.utility.local.IMammoth>, 'tiger')

  >>> component.getUtility(IPainting, name='blackandwhite')
  Traceback (most recent call last):
    ...
  ComponentLookupError: (<InterfaceClass grok.ftests.utility.local.IPainting>, 'blackandwhite')

  >>> component.getUtility(IPainting, name='color')
  Traceback (most recent call last):
    ...
  ComponentLookupError: (<InterfaceClass grok.ftests.utility.local.IPainting>, 'color')
"""
import grok
from zope import interface
import persistent

class IFireplace(interface.Interface):
    pass

class IClub(interface.Interface):
    pass

class ISpiky(interface.Interface):
    pass

class IMammoth(interface.Interface):
    pass

class Fireplace(grok.LocalUtility):
    grok.implements(IFireplace)

class Club(object):
    grok.implements(IClub)

class SpikyClub(object):
    grok.implements(IClub, ISpiky)

class Mammoth(grok.LocalUtility):
    grok.implements(IMammoth, IClub)

class SabretoothTiger(grok.LocalUtility):
    grok.implements(IMammoth, IClub)
    grok.provides(IMammoth)

class IPainting(persistent.interfaces.IPersistent):
    pass

class CavePainting(grok.LocalUtility):
    grok.implements(IPainting)

class ColoredCavePainting(grok.LocalUtility):
    grok.implements(IPainting)
    grok.provides(IPainting)

class Cave(grok.Model, grok.Site):
    grok.local_utility(Fireplace)
    grok.local_utility(Club)
    grok.local_utility(SpikyClub, provides=IClub, name='spiky')
    grok.local_utility(Mammoth, provides=IMammoth)
    grok.local_utility(SabretoothTiger, name='tiger')
    grok.local_utility(CavePainting, name='blackandwhite', provides=IPainting)
    grok.local_utility(ColoredCavePainting, name='color')
