"""
Grok allows you to set up catalog indexes in your application with a
special indexes declaration. In fact, we have multiple grok.Indexes
setting up more than one set of indexes in the same catalog.

Let's set up a site in which we manage a couple of objects::

  >>> herd = Herd()
  >>> getRootFolder()['herd'] = herd
  >>> from zope.site.hooks import setSite
  >>> setSite(herd)

We are able to query the catalog::

  >>> from zope.catalog.interfaces import ICatalog
  >>> from zope.component import getUtility, queryUtility
  >>> catalog = getUtility(ICatalog)
  >>> sorted(catalog.keys())
  [u'age', u'age2', u'message', u'message2', u'name', u'name2']
  
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

Unfortunately ftests don't have good isolation from each other yet.
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
    def message():
        """Message the mammoth has for the world."""

class IMammoth2(Interface):
    name2 = schema.TextLine(title=u'Name')
    age2 = schema.Int(title=u'Age')
    def message2():
        """Message the mammoth has for the world."""

class MammothIndexes(grok.Indexes):
    grok.site(Herd)
    grok.context(IMammoth)

    name = index.Field()
    age = index.Field()
    message = index.Text()

class MammothIndexes2(grok.Indexes):
    grok.site(Herd)
    grok.context(IMammoth2)

    name2 = index.Field()
    age2 = index.Field()
    message2 = index.Text()
