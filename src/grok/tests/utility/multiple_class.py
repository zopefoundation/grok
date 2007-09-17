"""
When you try to register multiple classes with the same (interface, name)
combination multiple times using grok.local_utility, we expect an error:

  >>> grok.grok(__name__)
  Traceback (most recent call last):
    ...
  GrokError: Conflicting local utility registration
  <class 'grok.tests.utility.multiple_class.Fireplace2'> in site
  <class 'grok.tests.utility.multiple_class.Cave'>.
  Local utilities are registered multiple times for interface
  <InterfaceClass grok.tests.utility.multiple_class.IFireplace> and
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
