"""
Global utilities can be created by subclassing grok.GlobalUtility:

  >>> grok.grok(__name__)
  >>> from zope import component

  >>> normal_club = component.getUtility(IClub)
  >>> IClub.providedBy(normal_club)
  True
  >>> isinstance(normal_club, NormalClub)
  True

Named utilities are registered using grok.name:

  >>> huge_club = component.getUtility(IClub, name='huge')
  >>> IClub.providedBy(huge_club)
  True
  >>> isinstance(huge_club, HugeClub)
  True

A utility can explicitly specify which interface it should be looked up with.

  >>> spiky_club = component.getUtility(IClub, name='spiky')
  >>> isinstance(spiky_club, SpikyClub)
  True

  >>> component.getUtility(ISpikyClub, name='spiky')
  Traceback (most recent call last):
    ...
  ComponentLookupError: (<InterfaceClass grok.tests.utility.utility.ISpikyClub>,
                         'spiky')

If a utility implements more than one interface, it has to specify the one to
use with 'grok.provides':

  >>> nightclub = component.getUtility(INightClub)
  >>> INightClub.providedBy(nightclub)
  True
  >>> isinstance(nightclub, NightClub)
  True
"""
import grok

from zope import interface

class IClub(interface.Interface):
    pass

class ISpikyClub(IClub):
    pass

class INightClub(interface.Interface):
    pass

class NormalClub(grok.GlobalUtility):
    grok.implements(IClub)

class HugeClub(grok.GlobalUtility):
    grok.implements(IClub)
    grok.name('huge')    

class SpikyClub(grok.GlobalUtility):
    grok.implements(ISpikyClub)
    grok.provides(IClub)
    grok.name('spiky')

class NightClub(grok.GlobalUtility):
    grok.implements(INightClub, ISpikyClub)
    grok.provides(INightClub)
