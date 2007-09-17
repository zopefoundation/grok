"""
  >>> grok.grok(__name__)
  Traceback (most recent call last):
    ...
  GrokError: Cannot determine which interface to use for utility registration of
  <class 'grok.tests.utility.local_implementsnone2.Fireplace'> in site
  <class 'grok.tests.utility.local_implementsnone2.Cave'>. It implements
  an interface that is a specialization of an interface implemented
  by grok.LocalUtility. Specify the interface by either using grok.provides on
  the utility or passing 'provides' to grok.local_utility.

"""

import grok
from zope import interface
import persistent

class ISpecialPersistent(persistent.interfaces.IPersistent):
    pass

class Fireplace(grok.LocalUtility):
    grok.implements(ISpecialPersistent)

class Cave(grok.Model, grok.Site):
    grok.local_utility(Fireplace)
