##############################################################################
#
# Copyright (c) 2007 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""
=================================
DocGrok: a class browser for Grok
=================================

DocGrok offers an extensible class browser for packages, modules,
classes and similar things. To use it in your own application see
``docgrok.txt`` in the ``grok.admin`` package.

Here only the functionality as a class browser for the admin-UI is
covered.

Overview page
-------------

When we go to the documentation section, we should get an overview:

  >>> from zope.testbrowser.testing import Browser
  >>> browser = Browser()
  >>> browser.addHeader('Authorization', 'Basic mgr:mgrpw')
  >>> browser.open('http://localhost/')
  >>> browser.getLink('Documentation').click()
  >>> print browser.contents
  <html xmlns="http://www.w3.org/1999/xhtml">
  ... Welcome to DocGrok...

The overview offers us direct links to the zope package,

  >>> link = browser.getLink('browse the zope package')
  >>> link
  <Link text='browse the zope package' url='http://localhost/docgrok/zope'>

the grok package,

  >>> link = browser.getLink('browse the grok package')
  >>> link
  <Link text='browse the grok package' url='http://localhost/docgrok/grok'>

and a link to the internal object browser, which is different from the
class browser, and shows the ZODB root:

  >>> link = browser.getLink('ZODB root folder')
  >>> link
  <Link text='ZODB root folder' url='http://localhost/@@inspect.html'>
  
There are several things, that can be displayed by the class
browser. We start with packages.


DocGrok for packages
--------------------

We placed a package in the ``apackage`` directory. Let's try to fetch
documentation for it. We form a URL string, that contains the
package's dotted name with dots replaced by slashes:

  >>> pkg_dotted_name = __name__.rsplit('.',1)[0]
  >>> url_path = 'http://localhost/docgrok/%s/apackage' % (
  ...    pkg_dotted_name.replace('.', '/'))
  >>> browser.open(url_path)

Is it the documentation of the ``apackage`` package?

  >>> print browser.contents
  <html xmlns="http://www.w3.org/1999/xhtml">
  ...
  ...<span><a ...>.apackage</a></span>...
  ...
  ...(Python Package)...
  ...

Okay. In the page top we should have links to the various parent
packages contained in the dotted name of the examined package:

  >>> browser.getLink('grok')
  <Link text='grok' url='http://localhost/docgrok/grok'>

  >>> browser.getLink('ftests')
  <Link text='.ftests' url='http://localhost/docgrok/grok/ftests'>

and so on.


DocGrok for modules
-------------------

DocGrok for classes
-------------------



"""
