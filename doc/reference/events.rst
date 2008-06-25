
******
Events
******

Grok provides convenient access to a set of often-used events from
Zope 3. Those events include object and containment events. All events
are available as interface and implemented class. All events interfaces
inherit from the base interface of `zope.component.interfaces.IObjectEvent`,
this interface has an attribute named object which is the subject of the
event taking place.

grok.IObjectModifiedEvent
=========================

An object has been modified. This is a general event that encompasses any
change to a persistent object, such as adding, moving, copying, and removing
of objects.

grok.IContainerModifiedEvent
============================

The container has been modified. Container modifications is specific to
addition, removal or reordering of sub-objects. Inherits from
`grok.IObjectModifiedEvent`.

grok.IObjectMovedEvent
======================

An object has been moved. This event provides attributes named oldParent, oldName,
newParent and newName that refer to the parent and name of the object both
before (old) and after (new) moving.

grok.IObjectAddedEvent
======================

An object has been added to a container. At this point the object provides
persistent location attributes (__name__ and __parent__). Inherits from
the `grok.IObjectMovedEvent`.

grok.IObjectCopiedEvent
=======================

An object has been copied. The event provides an attribute named `original`
which is a reference to the original object from which the copy was made.
Inherits from `grok.IObjectCreatedEvent`.

grok.IObjectCreatedEvent
========================

An object has been created. This event is intended to happen before an
object has been made persistent, so the object being created **does not**
yet provide location attributes (__name__ and __parent__).

grok.IObjectRemovedEvent
========================

An object has been removed from a container. Inherits from
`grok.IObjectMovedEvent`.

grok.ObjectModifiedEvent
========================

Default event implementation of the `grok.IObjectMovedEvent` interface.

Initialize this event with a list of modification descriptions::

	>>> import grok
	>>> from zope import event
	>>> from zope.interface import implements, Interface, Attribute
	>>> class ISample(Interface) :
	...     field = Attribute("A test field")
	>>> class Sample(object) :
	...     implements(ISample)

	>>> obj = Sample()
	>>> obj.field = 42
	>>> event.notify(
	... 	grok.ObjectModifiedEvent(
	... 		obj, Attributes(ISample, "field")
	... 	)
	... )

grok.ContainerModifiedEvent
===========================

Default event implementation of the `grok.IContainerModifiedEvent` interface.

Initialize this event with a list of modification descriptions, the same as
you would for a `grok.ObjectModifiedEvent`.

grok.ObjectMovedEvent
=====================

Default event implementation of the `grok.IObjectMovedEvent` interface.

Initialize this event with object, oldParent, oldName, newParent and newName
as positional arguments::

	>>> event.notify(
	... 	grok.ObjectMovedEvent(
	... 		obj, oldParent, oldName, newParent, newName
	... 	)
	... )

grok.ObjectAddedEvent
=====================

Default event implementation of the `grok.IObjectAddedEvent` interface.

Initialize this event with object, newParent and newName as positional
arguments::

	>>> event.notify(
	... 	grok.ObjectAddedEvent(obj, newParent, newName)
	... )

grok.ObjectCopiedEvent
======================

Default event implementation of the `grok.IObjectCopiedEvent` interface.

Initialize this event with the new copy and the original object as positional
arguments::

	>>> event.notify(
	... 	grok.ObjectCopiedEvent(copiedObject, originalObject)
	... )

grok.ObjectCreatedEvent
=======================

Default event implementation of the `grok.IObjectCreatedEvent` interface.

Initialize this event with the object created.

grok.ObjectRemovedEvent
=======================

Default event implementation of the `grok.IObjectRemovedEvent` interface.

Initialize this event with the object, oldParent, and oldName as
positional arguments.

