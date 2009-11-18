
******
Events
******

Grok provides convenient access to a set of often-used events from
Zope 3. Those events include object and containment events. All events
are available as interface and implemented class.

Subscription: Event interfaces
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

All events interfaces inherit from the base interface of IObjectEvent.

.. class:: zope.component.interfaces.IObjectEvent

    .. attribute:: object

        The subject of the event taking place.

:class:`IApplicationInitializedEvent`
=====================================

A Grok Application has been created with success and is now ready
to be used.

This event can be used to trigger the creation of contents or other tasks
that require the application to be fully operational : utilities installed
and indexes created in the catalog.

.. class:: grok.IApplicationInitializedEvent

    Interface to subscribe to application initialization.

    .. attribute:: object

        The application that has just been initialized.

:class:`IObjectModifiedEvent`
=============================

An object has been modified. This is a general event that encompasses any
change to a persistent object, such as adding, moving, copying, and removing
of objects.

.. class:: grok.IObjectModifiedEvent

    Interface to subscribe to for object modifications.

    .. attribute:: object

        The subject of the event.

    .. attribute:: descriptions

        A list of descriptions of the modifications.

:class:`IContainerModifiedEvent`
================================

The container has been modified. Container modifications is specific to
addition, removal or reordering of sub-objects. Inherits from
`grok.IObjectModifiedEvent`.

.. class:: grok.IContainerModifiedEvent

    Interface to subscribe to for container object modifications.

    .. attribute:: object

        The subject of the event.

    .. attribute:: descriptions

        A list of descriptions of the modifications.


:class:`IObjectMovedEvent`
==========================

An object has been moved.

.. class:: grok.IObjectMovedEvent

   Interface to subscribe to for when an object is moved.

   .. attribute:: object
      
      The subject of the event.
   
   .. attribute:: oldParent

      The container stored in before moving.

   .. attribute:: oldName

      The name before moving.
   
   .. attribute:: newParent

      The container stored in after moving.

   .. attribute:: newName
   
      The name after moving.

:class:`IObjectAddedEvent`
==========================

An object has been added to a container.

.. class:: grok.IObjectAddedEvent

   Interface to subscribe to for when an object is added to the database.
   
   Inherits from the `grok.IObjectMovedEvent` interface.

   .. attribute:: object
      
      The subject of the event.
   
   .. attribute:: oldParent

      The container stored in before moving.

   .. attribute:: oldName

      The name before moving.
   
   .. attribute:: newParent

      The container stored in after moving.

   .. attribute:: newName
   
      The name after moving.

:class:`IObjectCopiedEvent`
===========================

An object has been copied.

.. class:: grok.IObjectCopiedEvent

   Interface to subscribe to for when an object is cloned.

   Inherits from `grok.IObjectCreatedEvent` interface.

   .. attribute:: object
   
      The subject of the event.

   .. attribute:: original

      The original object from which the copy was made.


:class:`IObjectCreatedEvent`
============================

An object has been created. This event is intended to happen before an
object has been made persistent, that is it's location attributes
(__name__ and __parent__) will usually be None.

.. class:: grok.IObjectCreatedEvent

   Interface to subscribe to for when an object is created.

   .. attribute:: object
   
      The subject of the event.


:class:`IObjectRemovedEvent`
============================

An object has been removed from a container.

.. class:: grok.IObjectRemovedEvent

   Interface to subscribe to for object deletions.

   Inherits from `grok.IObjectMovedEvent`.

   .. attribute:: object
      
      The subject of the event.
   
   .. attribute:: oldParent

      The container stored in before removal.

   .. attribute:: oldName

      The name of the removed object.

:class:`IBeforeTraverseEvent`
=============================

The publisher is about to traverse into the object.

.. class:: grok.IBeforeTraverseEvent

   Interface to subscribe to for object traversal.
 
   .. attribute:: object
      
      The object being traversed throguh.

   .. attribute:: request

      The current request.

Notification: Event implementations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Event objects are notifications that are sent when need to "fire off" an event.

All of these event objects share the same minimal implementation of an event.
This class is defined at zope.component.interfaces.ObjectEvent and looks like
this:

.. code-block:: python

    from zope import interface
    
    class ObjectEvent(object):
        interface.implements(IObjectEvent)

        def __init__(self, object):
            self.object = object

:class:`ApplicationInitializedEvent`
=====================================

Event object to send after an application has been created.

.. class:: grok.ApplicationInitializedEvent

    Default event implementation of the `grok.IApplicationInitializedEvent` interface.

    .. attribute:: object

        The application that has just been initialized.

:class:`ObjectModifiedEvent`
============================

Event object to send as a notification when an object is modified.

.. class:: grok.ObjectModifiedEvent(object, *descriptions)

    Default event implementation of the `grok.IObjectMovedEvent` interface.

    .. attribute:: object

       The subject of the event.

    .. attribute:: descriptions
    
        A list of descriptions of the modifications.

**Example 1: Send an object modification event with a modified attribute
named "field".**

.. code-block:: python

    import grok
    import zope.event
    import zope.lifecycleevent.Attributes
    from zope.interface import Interface
    
    class ISample(Interface) :
        field = Attribute("A test field")
    
    class Sample(object) :
        grok.implements(ISample)

    obj = Sample()
    obj.field = 42
    zope.event.notify(
    	grok.ObjectModifiedEvent(obj,
    	zope.lifecycleevent.Attributes(ISample, "field"))
    )

:class:`ContainerModifiedEvent`
===============================

Event object to send as a notification when a container object modified.

.. class:: grok.ContainerModifiedEvent(object, *descriptions)

    Default event implementation of the `grok.IContainerModifiedEvent`
    interface.

    .. attribute:: object

       The subject of the event.

    .. attribute:: descriptions

        A list of descriptions of the modifications.


:class:`ObjectMovedEvent`
=========================

Event object to send as a notification of when an object is moved.

.. class:: grok.ObjectMovedEvent(object, oldParent, oldName, newParent, newName)

    Default event implementation of the `grok.IObjectMovedEvent` interface.

    .. attribute:: object

       The subject of the event.

    .. attribute:: oldParent

       The container stored in before moving.

    .. attribute:: oldName

       The name before moving.

    .. attribute:: newParent

       The container stored in after moving.

    .. attribute:: newName

       The name after moving.


:class:`ObjectAddedEvent`
=========================

Event object to send as a notification of when an object is added.

.. class:: grok.ObjectAddedEvent(object, newParent, newName)

    Default event implementation of the `grok.IObjectAddedEvent` interface.

    .. attribute:: object

       The subject of the event.

    .. attribute:: newParent

       The container stored in after moving.

    .. attribute:: newName

       The name after moving.


:class:`ObjectCopiedEvent`
==========================

Event object to send as a notification of when an object is copied.

.. class:: grok.ObjectCopiedEvent(object, original)

    Default event implementation of the `grok.IObjectCopiedEvent` interface.

    Initialize this event with the new copy and the original object as positional
    arguments.
    
    .. attribute:: object

       The subject of the event.

    .. attribute:: original

       The original object from which the copy was made.


:class:`ObjectCreatedEvent`
===========================

Event object to send as a notification of when an object is created.

.. class:: grok.ObjectCreatedEvent(object)

    Default event implementation of the `grok.IObjectCreatedEvent` interface.

    Initialize this event with the object created.

    .. attribute:: object

       The subject of the event.

:class:`grok.ObjectRemovedEvent`
================================

Event object to send as a notification of when an object is removed.

.. class:: grok.ObjectRemovedEvent*(object, oldParent, oldName)

    Default event implementation of the `grok.IObjectRemovedEvent` interface.

    .. attribute:: object
    
        The subject of the event.

    .. attribute:: oldParent

       The container stored in before removal.

    .. attribute:: oldName

       The name of the removed object.
