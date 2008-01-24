"""
Global utilities can be created by subclassing grok.GlobalUtility:

  >>> grok.testing.grok(__name__)
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

You can make the class the utility by providing the grok.direct() directive,
if you also use interface.classProvides instead of grok.provides.
This is useful for utilities that do nothing but create instances:

  >>> clubmaker = component.getUtility(IClubMaker, 'maker')
  >>> IClubMaker.providedBy(clubmaker)
  True
  >>> clubmaker is ClubMaker
  True

Utilities (including classes that do not subclass from grok.GlobalUtility) can
be (re-)registered using grok.global_utility:

  >>> fireplace = component.getUtility(IFireplace)
  >>> IFireplace.providedBy(fireplace)
  True
  >>> isinstance(fireplace, Fireplace)
  True

  >>> fireplace = component.getUtility(IFireplace, name='hot')
  >>> IFireplace.providedBy(fireplace)
  True
  >>> isinstance(fireplace, Fireplace)
  True

  >>> home = component.getUtility(IHome)
  >>> IHome.providedBy(home)
  True
  >>> isinstance(home, Home)
  True

  >>> night = component.getUtility(INightClub, name='cool')
  >>> IClub.providedBy(night)
  True
  >>> isinstance(night, NightClub)
  True
  
  >>> spiky = component.getUtility(ISpikyClub)
  >>> ISpikyClub.providedBy(spiky)
  True
  >>> isinstance(spiky, NightClub)
  True

When re-registering a grok.GlobalUtility, the directives grok.name and
grok.provides on the class will be used, but can be overriden in the
grok.global_utility directive:

  >>> small = component.getUtility(ISmallClub, name='tiny')
  >>> ISmallClub.providedBy(small)
  True
  >>> isinstance(small, SmallClub)
  True

  >>> small2 = component.getUtility(ITinyClub, name='tiny')
  >>> ISmallClub.providedBy(small2)
  True
  >>> isinstance(small2, SmallClub)
  True
  >>> small is not small2
  True

  >>> small3 = component.getUtility(ISmallClub, name='small')
  >>> ISmallClub.providedBy(small3)
  True
  >>> isinstance(small3, SmallClub)
  True
  >>> small3 is not small2 and small3 is not small
  True

Normally one registers a utility factory, such as the class, as a
global utility. It is also possible to register an arbitrary object directly
as a global utility. You do this by passing a 'direct' argument set to
'True'. This can be useful if one needs to register functions (such
as factory functions) that can be looked up as a utility, or if the
class you want to register as a global utility has an __init__ that
takes arguments, where you want to do the instantiation yourself.
Let's look up an instance we registered this way:

  >>> small4 = component.getUtility(ISmallClub, name='smallish')
  >>> ISmallClub.providedBy(small4)
  True
  >>> isinstance(small4, SmallClub)
  True
  
"""

import grok
from zope import interface

class IClub(interface.Interface):
    pass

class ISpikyClub(IClub):
    pass

class ISmallClub(IClub):
    pass

class ITinyClub(IClub):
    pass

class INightClub(interface.Interface):
    pass

class IClubMaker(interface.Interface):
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

class SmallClub(grok.GlobalUtility):
    grok.implements(ISmallClub, ITinyClub)
    grok.provides(ISmallClub)
    grok.name('tiny')

class ClubMaker(grok.GlobalUtility):
    grok.implements(IClub)
    interface.classProvides(IClubMaker)
    grok.direct()
    grok.name('maker')

class IFireplace(interface.Interface):
    pass

class IHome(interface.Interface):
    pass

class Fireplace(object):
    grok.implements(IFireplace)

class Home(object):
    grok.implements(IFireplace, IHome)

grok.global_utility(Fireplace)
grok.global_utility(Fireplace, name='hot')
grok.global_utility(Home, provides=IHome)

grok.global_utility(NightClub, name='cool')
grok.global_utility(NightClub, provides=ISpikyClub)

grok.global_utility(SmallClub, provides=ITinyClub)
grok.global_utility(SmallClub, name='small')

grok.global_utility(SmallClub(), name='smallish',
                    direct=True)
