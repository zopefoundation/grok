*********
Utilities
*********

The :mod:`grok.util` module provides functions which are less commonly
used, and so are not available for import directly from the :mod:`grok` module.

.. module:: grok.util

:func:`grok.util.application_url`
=================================

This function is also available as a method on the :class:`grok.View` class.

.. autofunction:: grok.util.application_url


:func:`grok.util.applySkin`
===========================

.. autofunction:: grok.util.applySkin


:func:`grok.util.create_application`
====================================

.. autofunction:: grok.util.create_application


:func:`grok.util.getApplication`
================================

This function is also exported to the main grok namespace and can be
called at :func:`grok.getApplication`.

.. autofunction:: grok.util.getApplication()

    .. deprecated:: 1.4
       This function has been moved to :mod:`grokcore.site`. Use
       :func:`grokcore.site.getApplication` instead.


:func:`grok.util.safely_locate_maybe`
=====================================

.. autofunction:: grok.util.safely_locate_maybe
