"""
A site can be created by mixing in grok.Site into a grok.Model or
grok.Container.

  >>> from zope import interface
  >>> from zope.location.interfaces import IPossibleSite, ISite
  >>> manfred = Mammoth()
  >>> IPossibleSite.providedBy(manfred)
  True
  >>> herd = Herd()
  >>> IPossibleSite.providedBy(herd)
  True
  >>> nonsite = NonSite()
  >>> IPossibleSite.providedBy(nonsite)
  False
  >>> nonsitecontainer = NonSiteContainer()
  >>> IPossibleSite.providedBy(nonsitecontainer)
  False

While manfred and herd are possible sites, they are not yet sites;

  >>> ISite.providedBy(manfred)
  False
  >>> ISite.providedBy(herd)
  False
  
When a site is added to a container it will be initialized as a site
(when the ObjectAddedEvent is fired):

  >>> nonsitecontainer['manfred'] = manfred
  >>> ISite.providedBy(manfred)
  True
  >>> nonsitecontainer['herd'] = herd
  >>> ISite.providedBy(herd)
  True
"""
import grok

class Mammoth(grok.Model, grok.Site):
    pass

class Herd(grok.Container, grok.Site):
    pass

class NonSite(grok.Model):
    pass

class NonSiteContainer(grok.Container):
    pass
