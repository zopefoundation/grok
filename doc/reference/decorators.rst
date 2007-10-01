
**********
Decorators
**********

grok uses a few decorators to register functions or methods for specific
functionality.


:func:`grok.subscribe` -- Register a function as a subscriber for an event
==========================================================================


.. function:: subscribe(*classes_or_interfaces)

   Declare that the decorated function subscribes to an event or a combination of
   objects and events and register it.

   Applicable on module-level for functions. Requires at least one class or
   interface as argument.

   (Similar to Zope 3's :func:`subscriber` decorator, but automatically performs
   the registration of the component.)


grok.action
===========

