*********
Utilities
*********

The :mod:`grok.util` module provides functions which are less commonly
used, and so are not available for import directly from the :mod:`grok` module.

:func:`grok.util.make_checker`
==============================

.. function:: grok.util.make_checker(factory, view_factory, permission, method_names=None)

    Make a checker for a view_factory associated with factory.

    These could be one and the same for normal views, or different
    in case we make method-based views such as for JSON and XMLRPC.

:func:`grok.util.safely_locate_maybe`
=====================================

.. function:: grok.util.safely_locate_maybe(obj, parent, name)

    Set an object's __parent__ (and __name__) if the object's
    __parent__ attribute doesn't exist yet or is None.

    If the object provides ILocation, __parent__ and __name__ will be
    set directly.  A location proxy will be returned otherwise.

:func:`grok.util.applySkin`
===========================

.. function:: grok.util.applySkin(request, skin, skin_type)

    Change the presentation skin for this request.

:func:`grok.util.create_application`
====================================

.. function:: grok.util.create_application(factory, container, name)

    Creates an application and triggers the events from
    the application lifecycle.
