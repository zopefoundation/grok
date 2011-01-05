*********
Functions
*********

The :mod:`grok` module provides a number of convenience functions to aid in
common tasks.


:func:`grok.AutoFields` -- deduce and return schema fields automatically
========================================================================

.. function:: grok.AutoFields(class_or_interface)

    This function is used inside :class:`Form` classes to automatically
    deduce the form fields from the schema of the `class_or_interface`.

This function is used to create a sequence of form fields from an interface
(schema) or from the interfaces (schemas) the context object provides.

**Example: Generate fields from an interface**

The :func:`grok.AutoFields` is used on the IMammoth interface, and all
attributes that inherit from IField (such as the ones supplied in the
zope.schema package) are concatenated into a list.

.. code-block:: python

     import grok
     from zope import interface, schema

     class IMammoth(interface.Interface):
         name = schema.TextLine(title=u"Name")
         size = schema.TextLine(title=u"Size", default=u"Quite normal")

     class Mammoth(grok.Model):
         interface.implements(IMammoth)

     class Edit(grok.EditForm):
         grok.context(Mammoth)

         form_fields = grok.AutoFields(Mammoth).omit('size')

In this example the ``size`` attribute will not show up in the resulting
edit view.

.. seealso::

    :class:`grok.EditForm`, :func:`grok.Fields`


:func:`grok.Fields` -- declare schema fields of a form
======================================================

.. function:: grok.Fields(*args, **kw)

   This function is used inside a :class:`grok.Fields` to generate fields
   (an object providing IFormFields) from positional and keyword arguments.
   These should be available in the definition order.

**Example: Generate form fields from schema objects**

When the :class:`Edit` form is rendered, the :class:`Textlines` `b` and `a`
will appear as input fields in that order.

.. code-block:: python

    import grok
    from zope import schema

    class Edit(grok.EditForm):
        fields = grok.Fields(
            b = schema.TextLine(title=u"Beta"),
            a = schema.TextLine(title=u"Alpha"),
        )

.. seealso::

    :func:`grok.AutoFields`, :class:`grok.Form`


:func:`grok.getApplication`
===========================

.. autofunction:: grok.getApplication()


:func:`grok.getSite`
====================

.. function:: grok.getSite()

    Get the current site object.

.. seealso::

    Site objects are instances of :class:`grok.Site`. Typically this will
    also be your main :class:`grok.Application` root object, which inherits
    from :class:`grok.Site`. Normally you will want to use
    `grok.getApplication` to get the application object, as `grok.getSite`
    can return enclosed sub-sites in applications with more complex
    configuration.

.. seealso::

    `Web Component Development With Zope 3, second edition <http://worldcookery.com/WhereToBuy>`_
    By Philipp von Weitershausen; Chapter 18 describes the use of Site objects.


:func:`grok.notify`
===================

.. function:: grok.notify(event)

   Send `event` to event subscribers.

**Example:**

.. code-block:: python

    import grok

    class Mammoth(object):
        def __init__(self, name):
            self.name = name

    manfred = Mammoth('manfred')

    grok.notify(grok.ObjectCreatedEvent(manfred))

.. seealso::

      Grok events provide a selection of common event types.

.. seealso::

    `Web Component Development With Zope 3, second edition <http://worldcookery.com/WhereToBuy>`_
    By Philipp von Weitershausen; Chapter 16 describes the Zope 3
    event system.


:func:`grok.url`
================

.. function:: grok.url(request, object, [, name])

    Construct a URL for the given `request` and `object`.

    `name` may be a string that gets appended to the object
    URL. Commonly used to construct an URL to a particular view on the
    object.

    This function returns the constructed URL as a string.

.. seealso::

    View classes derived from :class:`grok.View` have a similar
    :meth:`url` method for constructing URLs.

