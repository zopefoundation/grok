
*********
Functions
*********

The :mod:`grok` module provides a number of convenience functions to aid in
common tasks.


:func:`grok.getSite`
====================


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

