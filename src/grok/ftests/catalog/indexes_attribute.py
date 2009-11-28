"""
Grok allows you to set up catalog indexes in your application with a
special indexes declaration. If you want to name the index differently
from the attribute, you can do so, by passing an explicit `attribute`
keyword argument to the field.

Let's set up a site in which we manage a couple of objects::

  >>> herd = Herd()
  >>> getRootFolder()['herd'] = herd
  >>> from zope.site.hooks import setSite
  >>> setSite(herd)

Now we add some indexable objects to the site::

  >>> herd['alpha'] = Mammoth('Alpha', 13)
  >>> herd['beta'] = Mammoth('Beta', 14)

We are able to query the catalog::

  >>> from zope.catalog.interfaces import ICatalog
  >>> from zope.component import getUtility, queryUtility
  >>> catalog = getUtility(ICatalog)
  >>> for obj in catalog.searchResults(how_old=(13, 13)):
  ...   print obj.name
  Alpha

Nuke the catalog and intids in the end, so as not to confuse
other tests::

  >>> sm = herd.getSiteManager()
  >>> from zope.catalog.interfaces import ICatalog
  >>> sm.unregisterUtility(catalog, provided=ICatalog)
  True
  >>> from zope.intid.interfaces import IIntIds
  >>> from zope import component
  >>> intids = component.getUtility(IIntIds)
  >>> sm.unregisterUtility(intids, provided=IIntIds)
  True
"""

from zope.interface import Interface
from zope import schema

import grok
from grok import index

class Herd(grok.Container, grok.Application):
    pass

class IMammoth(Interface):
    name = schema.TextLine(title=u'Name')
    age = schema.Int(title=u'Age')

class MammothIndexes(grok.Indexes):
    grok.site(Herd)
    grok.context(IMammoth)

    name = index.Field()
    how_old = index.Field(attribute='age')

class Mammoth(grok.Model):
    grok.implements(IMammoth)

    def __init__(self, name, age):
        self.name = name
        self.age = age
