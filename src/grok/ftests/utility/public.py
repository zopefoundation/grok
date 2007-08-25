"""
By default, a utility is not in the public site; it's in ++etc++site. We can
also specify the utility to be public. It will then be created in the container
that is the site. The name the utility should have in the container can
be controlled using name_in_container:

  >>> cave = Cave()
  >>> getRootFolder()["cave"] = cave

  >>> from zope import component
  >>> from zope.app.component.hooks import getSite, setSite
  >>> setSite(cave)
  >>> cave['fireplace'] is component.getUtility(IFireplace)
  True

name_in_container can also be used for objects stored under the site manager
(that is in ++etc++site):

   >>> cave2 = Cave2()
   >>> getRootFolder()['cave2'] = cave2
   >>> setSite(cave2)
   >>> (cave2.getSiteManager()['fireplace'] is
   ...  component.getUtility(IFireplace))
   True

"""

import grok
from zope import interface

class IFireplace(interface.Interface):
    pass

class Fireplace(grok.LocalUtility):
    grok.implements(IFireplace)
    
class Cave(grok.Container, grok.Site):
    grok.local_utility(Fireplace, public=True, name_in_container='fireplace')

class Cave2(grok.Container, grok.Site):
    grok.local_utility(Fireplace, public=False, name_in_container='fireplace')
