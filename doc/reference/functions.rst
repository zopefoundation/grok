
*********
Functions
*********

The :mod:`grok` module provides a number of convenience functions to aid in
common tasks.


:func:`grok.AutoFields` -- Deduce and return schema fields automatically
========================================================================


.. function:: grok.AutoFields(class_or_interface)

   This function which can be used inside :class:`Form`
   classes to automatically deduce the form fields from the schema of
   the context `class_or_interface`.

   Different to most other directives, :func:`grok.AutoFields` is used
   more like a function and less like a pure declaration.

   This function is used to create a sequence of form fields from an interface
   (schema) or from the interfaces (schemas) the context object provides.

   The following example makes use of the :func:`grok.AutoFields`
   directive, in that one field is omitted from the form before
   rendering:

**Example:** ::

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

In this example the ``size`` attribute will not show up in the
resulting edit view.


.. seealso::

   :class:`grok.EditForm`, :func:`grok.Fields`

:func:`grok.Fields` -- declare schema fields of a form
======================================================

.. function:: grok.Fields(**schemas)

   A class level directive, which can be used inside :class:`grok.Form`
   classes.

   A :class:`grok.Fields` can receive keyword parameters with schema
   fields. These should be available in the definition order.

   **Example:** ::

      import grok
      from zope import schema

      class Mammoth(grok.Model):
          pass

      class Edit(grok.EditForm):
          fields = grok.Fields(
              b = schema.TextLine(title=u"Beta"),
              a = schema.TextLine(title=u"Alpha"),

   Given the above code, when the :class:`Edit` form is rendered, the
   :class:`Textlines` `b` and `a` will appear as input fields in that
   order. This is due to the fact, that by default the `fields`
   variable is taken into account, when rendering forms.

   .. seealso::

      :func:`grok.AutoFields`, :class:`grok.Form`

:func:`grok.getSite`
===============================================


.. function:: grok.getSite()

   Get the current site object.


   .. seealso::

      Site objects are instances of :class:`grok.Site` and/or
      :class:`grok.Application`.


   .. seealso::

      `Web Component Development With Zope 3, second edition <http://worldcookery.com/WhereToBuy>`_
         By Philiip von Weitershaussen; Chapter 18 describes the use of Site objects.


:func:`grok.notify`
===================


.. function:: grok.notify(event)

   Send `event` to event subscribers.

   Example::

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
         By Philiip von Weitershaussen; Chapter 16 describes the Zope 3 event system.


:func:`grok.url`
================


.. function:: grok.url(request, object, [, name])

   Construct a URL for the given `request` and `object`.

   `name` may be a string that gets appended to the object URL. Commonly used to
   construct an URL to a particular view on the object.

   This function returns the constructed URL as a string.


   .. seealso::

      View classes derived from :class:`grok.View` have a similar :meth:`url` method
      for constructing URLs.


:func:`grok.grok` -- Grok a package or module
=============================================


.. function:: grok(dotted_name)

.. note:: Usually you don't need to invoke this funtion in your code, since it's triggered from the `configure.zcml`. Grokking test fixtures is one  situation where it is useful to call this explicitly.

Grokking a package or module activates the contained components (like models,
views, adapters, templates, etc.) and registers them with Zope 3's component
architecture.

The `dotted_name` must specify either a Python module or package that is
available from the current PYTHONPATH.

Grokking a module:

#. Scan the module for known components: models, adapters, utilities, views,
      traversers, templates and subscribers.

#. Check whether a directory with file system templates exists
(:file:`<modulename>_templates`). If it exists, load the file system templates
into the template registry for this module.

#. Determine the module context.

#. Register all components with the Zope 3 component architecture.

#. Initialize schemata for registered models

   Grokking a package:

#. Grok the package as a module.

#. Check for a static resource directory (:file:`static`) and register it if
it exists.

#. Recursively grok all sub-modules and sub-packages.


