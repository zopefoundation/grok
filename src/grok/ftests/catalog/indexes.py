"""
Grok allows you to set up catalog indexes in your application with a
special indexes declaration.

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
  >>> from zope.component import getUtility, queryUtility
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

Note that another application that we did not register the
indexes for won't have a catalog available::

  >>> herd2 = Herd2()
  >>> getRootFolder()['herd2'] = herd2
  >>> setSite(herd2)
  >>> queryUtility(ICatalog, default=None) is None
  True
  >>> setSite(herd)
  
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

from zope.interface import Interface
from zope import schema

import grok
from grok import index

class Herd(grok.Container, grok.Application):
    pass

class Herd2(grok.Container, grok.Application):
    pass

class IMammoth(Interface):
    name = schema.TextLine(title=u'Name')
    age = schema.Int(title=u'Age')
    def message():
        """Message the mammoth has for the world."""

class MammothIndexes(grok.Indexes):
    grok.site(Herd)
    grok.context(IMammoth)

    name = index.Field()
    age = index.Field()
    message = index.Text()

class Mammoth(grok.Model):
    grok.implements(IMammoth)

    def __init__(self, name, age, message):
        self.name = name
        self.age = age
        self._message = message

    def message(self):
        return self._message
    
