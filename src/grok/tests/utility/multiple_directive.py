"""
When you call the grok.local_utility directive multiple times specifying
the same (interface, name) combination, we expect an error:

  >>> grok.grok(__name__)
  Traceback (most recent call last):
    ...
  GrokError: Conflicting local utility registration
  <class 'grok.tests.utility.multiple_directive.Fireplace2'> in site
  <class 'grok.tests.utility.multiple_directive.Cave'>.
  Local utilities are registered multiple times for interface
  <InterfaceClass grok.tests.utility.multiple_directive.IFireplace> and
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
