"""
When you call the grok.local_utility directive multiple times specifying
the same (interface, name) combination, we expect an error:

  >>> import grok
  >>> from zope import component
  >>> from grok.ftests.utility.multiple_directive import *

  >>> grok.grok('grok.ftests.utility.multiple_directive')
  Traceback (most recent call last):
    ...
  GrokError: Conflicting local utility registration
  <class 'grok.ftests.utility.multiple_directive.Fireplace2'> in site
  <class 'grok.ftests.utility.multiple_directive.Cave'>.
  Local utilities are registered multiple times for interface
  <InterfaceClass grok.ftests.utility.multiple_directive.IFireplace> and
  name u''.  
"""
import grok
from zope import interface

class IFireplace(interface.Interface):
    pass

class Fireplace(grok.LocalUtility):
    grok.implements(IFireplace)

class Fireplace2(grok.LocalUtility):
    grok.implements(IFireplace)
    
class Cave(grok.Model, grok.Site):
    grok.local_utility(Fireplace, provides=IFireplace)
    grok.local_utility(Fireplace2, provides=IFireplace)
