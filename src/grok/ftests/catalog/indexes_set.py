"""
We now demonstrate the use of a SetIndex with Grok::

Let's set up a site in which we manage a couple of objects::

  >>> herd = Herd()
  >>> getRootFolder()['herd'] = herd
  >>> from zope.app.component.hooks import setSite
  >>> setSite(herd)

Now we add some indexable objects to the site::

  >>> herd['alpha'] = Mammoth('Alpha', ['big', 'brown'])
  >>> herd['beta'] = Mammoth('Beta', ['big', 'black', 'friendly'])
  >>> herd['gamma'] = Mammoth('Gamma', ['brown', 'friendly', 'gorgeous'])

Let's query the set index::

  >>> from zope.app.catalog.interfaces import ICatalog
  >>> from zope.component import getUtility, queryUtility
  >>> catalog = getUtility(ICatalog)
  >>> def sortedResults(catalog, **kw):
  ...    result = list(catalog.searchResults(**kw))
  ...    result.sort(key=lambda x:x.name)
  ...    return [item.name for item in result]
  >>> sortedResults(catalog, features={'any_of': ['brown']})
  ['Alpha', 'Gamma']
  >>> sortedResults(catalog, features={'any_of': ['big']})
  ['Alpha', 'Beta']
  >>> sortedResults(catalog, features={'any_of': ['friendly']})
  ['Beta', 'Gamma']
  
Nuke the catalog and intids in the end, so as not to confuse
other tests::

  >>> sm = herd.getSiteManager()
  >>> from zope.app.catalog.interfaces import ICatalog
  >>> sm.unregisterUtility(catalog, provided=ICatalog)
  True
  >>> from zope.app.intid.interfaces import IIntIds
  >>> from zope import component
  >>> intids = component.getUtility(IIntIds)
  >>> sm.unregisterUtility(intids, provided=IIntIds)
  True

Unfortunately ftests don't have good isolation from each other yet.
"""

from zope.interface import Interface, Attribute
from zope import schema

import grok
from grok import index

class Herd(grok.Container, grok.Application):
    pass

class IMammoth(Interface):
    features = Attribute('Features')
    
class MammothIndexes(grok.Indexes):
    grok.site(Herd)
    grok.context(IMammoth)

    features = index.Set()

class Mammoth(grok.Model):
    grok.implements(IMammoth)

    def __init__(self, name, features):
        self.name = name
        self.features = features
    
