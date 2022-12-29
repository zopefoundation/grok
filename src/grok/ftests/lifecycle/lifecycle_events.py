"""
==============================
Application lifecycle overview
==============================

The application initialization is an important moment of your
application's life. This creation process is responsible for the
local utilities and the catalog indexes' creation. Let's create a site
to demonstrate the different steps.


  >>> root = getRootFolder()

The life cycle of an application is made of 2 major events :
ObjectCreatedEvent and ObjectAddedEvent.

ObjectCreatedEvent shoud be triggered when an application is
instanciated. At this step, the application doesn't have a site
manager yet.

  >>> from zope.component.hooks import setSite

  >>> site = Herd()
  >>> grok.notify(grok.ObjectCreatedEvent(site))
  >>> setSite(site)
  Traceback (most recent call last):
  ...
  zope.interface.interfaces.ComponentLookupError: no site manager defined

As the application is instanciated and notified as "created", we can
now persist it. This operation will fire the "ObjectAddedEvent". This
event is trigged by the container and the associated event handlers
will create the site manager. Once the site manager is created, Grok's
subscribers will create the local utilities and the indexes.

This particular step is often used to trigger the creation of
content. However, as the event handlers are not ordered, we can not be
sure that our handler will be called after the local utilities
creation. This can be quite annoying : the content created by our
handler may not be regitered in the Catalog and the IntIds utility.

To demonstrate this behavior, we now persist the application. This
will trigger a test handler that queries the Catalog::

  >>> root['site'] = site
  Catalog can not be found !

Now our application is persisted, the site manager and the local
utilities are created. We can safely use our application. An event is
provided by Grok, to be fired at this step. The same test event shows
that we can now work on an operational environment:

  >>> grok.notify(grok.ApplicationAddedEvent(site))
  <zope.catalog.catalog.Catalog object at ...>

"""
from zope.catalog.interfaces import ICatalog
from zope.component import queryUtility
from zope.interface import Interface
from zope.schema import TextLine

import grok
from grok import index


class Herd(grok.Container, grok.Application):
    pass


class IPachyderm(Interface):
    tusks = TextLine(title="About the tusks")


class TuskIndex(grok.Indexes):
    grok.context(IPachyderm)
    grok.site(Herd)

    tusks = index.Text()


@grok.subscribe(Herd, grok.IObjectAddedEvent)
@grok.subscribe(Herd, grok.IApplicationAddedEvent)
def CatalogTester(application, event):
    catalog = queryUtility(ICatalog, context=application)
    if catalog is None:
        print("Catalog can not be found !")
    else:
        print(catalog)
