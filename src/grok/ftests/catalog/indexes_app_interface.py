"""
Grok allows you to set up catalog indexes in your application with a
special indexes declaration. Here we see how we can register indexes for
an interface instead of an application directly.

Let's set up a site in which we manage a couple of objects::

  >>> herd = Herd()
  >>> getRootFolder()['herd'] = herd
  >>> from zope.site.hooks import setSite
  >>> setSite(herd)

We are able to find the catalog::

  >>> from zope.catalog.interfaces import ICatalog
  >>> from zope.component import getUtility
  >>> catalog = getUtility(ICatalog)
  >>> catalog is not None
  True
  >>> catalog.get('name') is not None
  True

Nuke the catalog and intids for this site, so as not to confuse
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

Now let's create another application providing the same interface::

  >>> herd2 = Herd2()
  >>> getRootFolder()['herd2'] = herd2
  >>> setSite(herd2)
  >>> catalog = getUtility(ICatalog)
  >>> catalog is not None
  True
  >>> catalog.get('name') is not None
  True
  
Nuke the catalog and intids in the end, so as not to confuse
other tests::

  >>> sm = herd2.getSiteManager()
  >>> sm.unregisterUtility(catalog, provided=ICatalog)
  True
  >>> intids = component.getUtility(IIntIds)
  >>> sm.unregisterUtility(intids, provided=IIntIds)
  True
"""

from zope.interface import Interface
from zope import schema

import grok
from grok import index


class IHerd(Interface):
    pass


class Herd(grok.Container, grok.Application):
    grok.implements(IHerd)


class Herd2(grok.Container, grok.Application):
    grok.implements(IHerd)


class IMammoth(Interface):
    name = schema.TextLine(title=u'Name')
    age = schema.Int(title=u'Age')
    def message():
        """Message the mammoth has for the world."""


class MammothIndexes(grok.Indexes):
    grok.site(IHerd)
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
