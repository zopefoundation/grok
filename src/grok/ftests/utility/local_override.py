"""
Local Utilities can be registered on subclasses of grok.Site using
grok.local_utility:

  >>> import grok
  >>> from zope import component
  >>> from grok.ftests.utility.local_override import *

  >>> grok.grok('grok.ftests.utility.local_override')

  >>> cave = SpikyCave()
  >>> getRootFolder()['cave'] = cave

  >>> from zope.app.component.hooks import getSite, setSite
  >>> setSite(cave)

  >>> club = component.getUtility(IClub)
  >>> IClub.providedBy(club)
  True
  >>> isinstance(club, SpikyClub)
  True

  >>> list(cave.getSiteManager().keys())
  [u'SpikyClub']
"""
import grok
from zope import interface
import persistent

class IClub(interface.Interface):
    pass

class Club(grok.LocalUtility):
    grok.implements(IClub)

class SpikyClub(grok.LocalUtility):
    grok.implements(IClub)

class Cave(grok.Model, grok.Site):
    grok.local_utility(Club)

class SpikyCave(Cave):
    grok.local_utility(SpikyClub)

