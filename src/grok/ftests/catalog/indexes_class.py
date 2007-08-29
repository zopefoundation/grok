"""
Grok allows you to set up catalog indexes in your application with a
special indexes declaration. This can also be done without explicit interface.
The context of the indexes applies to a class in this case.

Let's set up a site in which we manage a couple of objects::

  >>> herd = Herd()
  >>> getRootFolder()['herd'] = herd
  >>> from zope.app.component.hooks import setSite
  >>> setSite(herd)

Now we add some indexable objects to the site::

  >>> herd['alpha'] = Mammoth('Alpha', 13, 'Hello world!')
  >>> herd['beta'] = Mammoth('Beta', 14, 'Bye World!')

We are able to query the catalog::

  >>> from zope.app.catalog.interfaces import ICatalog
  >>> from zope.component import getUtility
  >>> catalog = getUtility(ICatalog)
  >>> for obj in catalog.searchResults(name=('Beta', 'Beta')):
  ...   print obj.name
  Beta

Let's query the text index, which incidentally also indexes a method::

  >>> def sortedResults(catalog, **kw):
  ...    result = list(catalog.searchResults(**kw))
  ...    result.sort(key=lambda x:x.name)
  ...    return [item.name for item in result]
  >>> sortedResults(catalog, message='world')
  ['Alpha', 'Beta']
  >>> sortedResults(catalog, message='hello')
  ['Alpha']
  >>> sortedResults(catalog, message='bye')
  ['Beta']
  
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
import grok
from grok import index

class Herd(grok.Container, grok.Application):
    pass

class Mammoth(grok.Model):
    def __init__(self, name, age, message):
        self.name = name
        self.age = age
        self._message = message

    def message(self):
        return self._message

class MammothIndexes(grok.Indexes):
    grok.context(Mammoth)
    grok.site(Herd)
    
    name = index.Field()
    age = index.Field()
    message = index.Text()

