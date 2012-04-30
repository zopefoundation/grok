"""
Grok allows you to set up catalog indexes in your application with a
special indexes declaration. Here we show what happens if you try
to set up an index for an attribute that does not exist on the interface.

Let's set up a site in which we manage a couple of objects::

  >>> herd = Herd()
  >>> getRootFolder()['herd'] = herd
  Traceback (most recent call last):
    ...
  GrokError: grokcore.catalog.Indexes in <module
  'grok.ftests.catalog.indexes_nonexistent' from ...>
  refers to an attribute or method 'foo' on interface <InterfaceClass
  grok.ftests.catalog.indexes_nonexistent.IMammoth>, but this does not
  exist.

Nuke the catalog and intids in the end, so as not to confuse
other tests::

  >>> from zope.site.hooks import setSite
  >>> setSite(herd)
  >>> from zope.catalog.interfaces import ICatalog
  >>> from zope.component import getUtility
  >>> catalog = getUtility(ICatalog)


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
    def message():
        """Message the mammoth has for the world."""

class MammothIndexes(grok.Indexes):
    grok.site(Herd)
    grok.context(IMammoth)

    foo = index.Field()



