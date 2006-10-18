"""
Global utilities can be created by subclassing grok.Utility:

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
"""
import grok

from zope import interface

class IClub(interface.Interface):
    pass

class NormalClub(grok.Utility):
    grok.implements(IClub)

class HugeClub(grok.Utility):
    grok.implements(IClub)
    grok.name('huge')    
