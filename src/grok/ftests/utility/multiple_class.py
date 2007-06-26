"""
When you try to register multiple classes with the same (interface, name)
combination multiple times using grok.local_utility, we expect an error:

  >>> import grok
  >>> from zope import component
  >>> from grok.ftests.utility.multiple_class import *

  >>> grok.grok('grok.ftests.utility.multiple_class')
  Traceback (most recent call last):
    ...
  GrokError: Conflicting local utility registration
  <class 'grok.ftests.utility.multiple_class.Fireplace2'> in site
  <class 'grok.ftests.utility.multiple_class.Cave'>.
  Local utilities are registered multiple times for interface
  <InterfaceClass grok.ftests.utility.multiple_class.IFireplace> and
  name 'Foo'.  
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
    grok.local_utility(Fireplace, name='Foo')
    grok.local_utility(Fireplace2, name='Foo')
