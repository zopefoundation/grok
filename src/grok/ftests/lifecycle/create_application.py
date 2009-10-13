"""
====================
Application creation
====================

The application creation can be handled by Grok. In order to setup a
functional application, the creation method will go through all the
needed events : ObjectCreated, ObjectAdded, ApplicationInitialized.

Let's create our environment. We are at the zope instance root folder.

  >>> root = getRootFolder()

In this folder, we want our Cave applicate. To create it, Grok
provides a convenient function called `create_application`::

  >>> import grok.util
  >>> app = grok.util.create_application(Cave, root, 'mycave')
  Cave <zope.app.event.objectevent.ObjectCreatedEvent object at ...>
  Cave <zope.app.container.contained.ObjectAddedEvent object at ...>
  Cave <grok.events.ApplicationInitializedEvent object at ...>

As we can see, the events are effectively trigged, and in the right
order. The function returns the persisted application method.

  >>> print app
  <grok.ftests.lifecycle.create_application.Cave object at ...>
  >>> print app.__parent__
  <zope.app.folder.folder.Folder object at ...>

However, if an error occur during the creation process, the exception
is not caught by `create_application`.

In the case we provide an id that already exists, the exception will
be raised *BEFORE* the application instanciation. For this reason, and
intentionally, no event will be trigged.

  >>> app = grok.util.create_application(Cave, root, 'mycave')
  Traceback (most recent call last):
  ...
  DuplicationError: mycave

Please note that the `create_application` function will only accept
factories implementing IApplication::

  >>> james = grok.util.create_application(Mammoth, root, 'james')
  Traceback (most recent call last):
  ...
  WrongType: <class 'grok.ftests.lifecycle.create_application.Mammoth'>

"""
import grok


class Mammoth(grok.Model):
    """A furry creature with tusks.
    """
    pass

class Cave(grok.Container, grok.Application):
    """A shelter for the homeless cavemen.
    """
    pass

@grok.subscribe(Cave, grok.IObjectCreatedEvent)
@grok.subscribe(Cave, grok.IObjectAddedEvent)
@grok.subscribe(Cave, grok.IApplicationInitializedEvent)
def EventPrinter(application, event):
    print application.__class__.__name__, event
