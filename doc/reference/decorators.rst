**********
Decorators
**********

Grok uses a few decorators to register functions or methods for specific
functionality.


:func:`grok.subscribe` -- register a function as a subscriber for an event
==========================================================================

.. function:: subscribe(*classes_or_interfaces)

    Declare that the decorated function subscribes to an event or a
    combination of objects and events.

    Applicable on module-level for functions. Requires at least one
    class or interface as argument.


:func:`grok.action` -- declare a form submit handler
=====================================================

.. function:: action(label, **options)

    Decorator that defines an action factory based on a form
    method. The method receives the form data as keyword
    parameters.


:func:`grok.require` -- protect a method with a permission
==========================================================

.. function:: require(name_or_class)

    The decorated method will be protected by the permission. Used in
    web service views such as REST or XML-RPC.


:func:`grok.adapter/grok.implementer` -- declare an adapter factory
====================================================================

These decorators are always used in tandem to declare an adapter factory.

.. function:: grok.adapter(*classes_or_interfaces) 

    Describes that a function adapts an object or a combination
    of objects.

.. function:: grok.implementer(interface) 

    Describes that a function that's used as an adapter
    implements an interface or a number of interfaces.


**Example 1: Adapt to an interface**

.. code-block:: python

	@grok.adapter(ICave)
	@grok.implementer(IHome)
	def home_for_cave(cave):
	    return Home()

**Example 2: Adapt a regular class instead of an interface**

.. code-block:: python

	@grok.adapter(Cave)
	@grok.implementer(IHome)
	def home_for_cave(cave):
	    return Home()

**Example 3: Declare a multi-adapter factory**

.. code-block:: python

	@grok.adapter(ICave, IFire)
	@grok.implementer(ICozy)
	def cozy_dwelling(cave, fire):
	    return Dwelling()

