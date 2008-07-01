grok.admin.introspector
***********************

Introspect objects and applications.

:Test-Layer: functional

Introduction
============

The grokadmin introspector is built upon ``zope.introspector``. Its
purpose is to deliver in-depth information about applications, objects
and other thing existing in a running Grok environment.

Unlike ``zope.introspector`` this package also provides viewing
components to display all the information retrieved. Furthermore we
have the opportunity to get informed about aspects, which are specific
for Grok and/or Zope 3 like lists of available directives, used
grokkers etc.

The Grok introspector is context-oriented. That means, that it is able
to provide information about objects in specific contexts, so that you
can for example get a list of available views in the context of a
given skin/layer.

Basic Usage
===========

Although the Grok introspector is context-oriented, it also provides
an overview page as a starting point for general explorations of the
whole runtime environment.

Before we can access any pages, we have to initialize the test
browser::

  >>> from zope.testbrowser.testing import Browser
  >>> browser = Browser()
  >>> browser.addHeader('Authorization', 'Basic mgr:mgrpw')
  >>> browser.handleErrors = False

All introspector related content is shown in a special skin called
``introspector``, so that you can enter the follwing URL to access the
overview page::

  >>> browser.open('http://localhost/++skin++introspector/')
  >>> print browser.contents
  <!DOCTYPE html...
  <h1>The Grok Introspector</h1>
  ...

Note the `++skin++introspector` marker in the URL.

