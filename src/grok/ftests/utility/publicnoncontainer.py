"""
You cannot use local_utility with 'public' set to True if the site class
isn't a container:

  >>> import grok
  >>> from zope import component
  >>> from grok.ftests.utility.publicnoncontainer import *
  >>> grok.grok('grok.ftests.utility.publicnoncontainer')
  Traceback (most recent call last):
    ...
  GrokError: Cannot set public to True with grok.local_utility as the site
  (<class 'grok.ftests.utility.publicnoncontainer.Cave'>) is not a container.

"""

import grok
from zope import interface

class IFireplace(interface.Interface):
    pass

class Fireplace(grok.LocalUtility):
    grok.implements(IFireplace)
    
class Cave(grok.Model, grok.Site):
    grok.local_utility(Fireplace, public=True, name_in_container='fireplace')
