"""
Let's setup a site in which we manage a couple of objects:

  >>> herd = Herd()
  >>> getRootFolder()['herd'] = herd
  >>> from zope.app.component.hooks import setSite
  >>> setSite(herd)

Now we add some indexable objects to the site:

  >>> herd['manfred'] = Mammoth('Manfred')
  >>> herd['ellie'] = Mammoth('Ellie')

Then we are able to query the catalog:

  >>> from zope.app.catalog.interfaces import ICatalog
  >>> from zope.component import getUtility
  >>> catalog = getUtility(ICatalog)
  >>> for obj in catalog.searchResults(name=('Ellie', 'Ellie')):
  ...     print obj.name
  Ellie

"""

import grok
from zope import schema, interface
from zope.app.intid import IntIds
from zope.app.intid.interfaces import IIntIds
from zope.app.catalog.catalog import Catalog
from zope.app.catalog.interfaces import ICatalog
from zope.app.catalog.field import FieldIndex

def setup_catalog(catalog):
    catalog['name'] = FieldIndex('name', IMammoth)

class IMammoth(interface.Interface):

    name = schema.TextLine()

class Mammoth(grok.Model):
    grok.implements(IMammoth)

    def __init__(self, name):
        self.name = name

class Herd(grok.Container, grok.Site):
    grok.local_utility(IntIds, provides=IIntIds)
    grok.local_utility(Catalog, provides=ICatalog, setup=setup_catalog)
