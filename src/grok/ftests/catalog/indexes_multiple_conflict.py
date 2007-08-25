"""
Grok allows you to set up catalog indexes in your application with a
special indexes declaration. In fact, we have multiple grok.Indexes
setting up more than one set of indexes in the same catalog. What if these
indexes define the same names?

Let's set up a site in which we manage a couple of objects::

  >>> herd = Herd()
  >>> getRootFolder()['herd'] = herd
  Traceback (most recent call last):
    ...
  GrokError: grok.Indexes in module <module
  'grok.ftests.catalog.indexes_multiple_conflict' from ...>
  causes creation of catalog index 'name' in catalog u'', but an index
  with that name is already present.

  >>> from zope.app.component.hooks import setSite
  >>> setSite(herd)
  >>> from zope.app.catalog.interfaces import ICatalog
  >>> from zope.component import getUtility, queryUtility
  >>> catalog = getUtility(ICatalog)

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

class IMammoth(Interface):
    name = schema.TextLine(title=u'Name')

class IMammoth2(Interface):
    name = schema.TextLine(title=u'Name')

class MammothIndexes(grok.Indexes):
    grok.site(Herd)
    grok.context(IMammoth)

    name = index.Field()

class MammothIndexes2(grok.Indexes):
    grok.site(Herd)
    grok.context(IMammoth2)

    name = index.Field()
