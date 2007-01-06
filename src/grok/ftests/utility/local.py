"""
Local Utilities can be registered on subclasses of grok.Site using
grok.local_utility:

  >>> import grok
  >>> from zope import component
  >>> from grok.ftests.utility.local import Cave, Fireplace, IFireplace

  >>> grok.grok('grok.ftests.utility.local')

  >>> cave = Cave()
  >>> getRootFolder()["cave"] = cave

  >>> from zope.app.component.hooks import getSite, setSite
  >>> setSite(cave)
  >>> fireplace = component.getUtility(IFireplace)
  >>> IFireplace.providedBy(fireplace)
  True
  >>> isinstance(fireplace, Fireplace)
  True

Since it is a local utility, it is not available outside its site:

  >>> setSite(None)
  >>> component.getUtility(IFireplace)
  Traceback (most recent call last):
    ...
  ComponentLookupError: (<InterfaceClass grok.ftests.utility.local.IFireplace>, '')
"""
import grok
from zope import interface

class IFireplace(interface.Interface):
    pass

class Fireplace(grok.LocalUtility):
    grok.implements(IFireplace)

class Cave(grok.Model, grok.Site):
    grok.local_utility(Fireplace, provides=IFireplace)
