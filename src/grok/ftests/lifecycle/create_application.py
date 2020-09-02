"""
====================
Application creation
====================

The application creation can be handled by Grok. In order to setup a
functional application, the creation method will go through all the
needed events : ObjectCreated, ObjectAdded, ApplicationAdded.

Let's create our environment. We are at the zope instance root folder.

  >>> root = getRootFolder()

In this folder, we want our Cave applicate. To create it, Grok
provides a convenient function called `create_application`::

  >>> app = grok.create_application(Cave, root, 'mycave')
  Cave <zope.lifecycleevent.ObjectCreatedEvent object at ...>
  Cave <zope.lifecycleevent.ObjectAddedEvent object at ...>
  Cave <grokcore.site.interfaces.ApplicationAddedEvent object at ...>

As we can see, the events are effectively trigged, and in the right
order. The function returns the persisted application.

  >>> app
  <grok.ftests.lifecycle.create_application.Cave object at ...>
  >>> app.__parent__
  <zope.site.folder.Folder object at ...>

However, if an error occurs during the creation process, the exception
is not caught by `create_application`.

In the case we provide an id that already exists, the exception will
be raised *BEFORE* the application instanciation. For this reason, and
intentionally, no event will be trigged.

  >>> app = grok.create_application(Cave, root, 'mycave')
  Traceback (most recent call last):
  ...
  KeyError: 'mycave'

Please note that the `create_application` function will only accept
factories implementing IApplication::

  >>> james = grok.create_application(Mammoth, root, 'james')
  Traceback (most recent call last):
  ...
  zope.schema._bootstrapinterfaces.WrongType: <class 'grok.ftests.lifecycle.create_application.Mammoth'>

"""  # noqa: E501
from __future__ import print_function
import grok


class Mammoth(grok.Model):
    """A furry creature with tusks.
    """
    pass


class Cave(grok.Container, grok.Application):
    """A shelter for homeless cavemen.
    """
    pass


@grok.subscribe(Cave, grok.IObjectCreatedEvent)
@grok.subscribe(Cave, grok.IObjectAddedEvent)
@grok.subscribe(Cave, grok.IApplicationAddedEvent)
def EventPrinter(application, event):
    print(application.__class__.__name__, event)
