
**********
Decorators
**********

grok uses a few decorators to register functions or methods for specific
functionality.


:func:`grok.subscribe` -- Register a function as a subscriber for an event
==========================================================================


.. function:: subscribe(*classes_or_interfaces)

  Declare that the decorated function subscribes to an event or a
  combination of objects and events and register it.

  Applicable on module-level for functions. Requires at least one
  class or interface as argument.

  (Similar to Zope 3's :func:`subscriber` decorator, but automatically
  performs the registration of the component.)


:func:`grok.action` -- Declare a form submit handler
=====================================================


:func:`grok.require` -- Protect a method with a permission
===========================================================

:func:`grok.adapter/grok.implementer` -- Declare an adapter factory
====================================================================

.. XXX these two decorators are always used together, but are named
   separately because they are separate in the Zope 3 API. Should
   grok implement this as one decorator with two arguments?

These decorators are always used in tandem to declare an adapter factory.

.. function:: grok.adapter(*interfaces) 

  `*interfaces` -- the interfaces *adapted* by the object created by
                   this factory.


.. function:: grok.implementer(interface) 

  `interface` -- the interface *provided* by the object created by
                 this factory.


**Example 1:**

.. code-block:: python

	@grok.adapter(ICave)
	@grok.implementer(IHome)
	def home_for_cave(cave):
	    return Home()

**Example 2: adapt a regular class instead of an interface**

.. code-block:: python

	@grok.adapter(Cave)
	@grok.implementer(IHome)
	def home_for_cave(cave):
	    return Home()

**Example 3: declare a multi-adapter factory**

.. code-block:: python

	@grok.adapter(ICave,IFire)
	@grok.implementer(ICozy)
	def cozy_dwelling(cave, fire):
	    return Dwelling()

