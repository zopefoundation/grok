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

A standard package, that should always be reachable, is the ``zope``
package::

  >>> browser.open('http://localhost:8080/docgrok/zope')
  >>> print browser.contents
  <html xmlns="http://www.w3.org/1999/xhtml">
  ...
  ...<span><a ...>zope</a></span>...
  ...
  ...(Python Package)...
  ...
  

DocGrok for modules
-------------------

DocGrok for classes
-------------------

Custom DocGroks
---------------

It is relatively easy to provide own DocGroks, that are displayed when
browsing. You have to provide three parts:

* a DocGrok class

* a DocGrokHandlerClass

* a view for the DocGrok class

The latter is optional, but required, if you want to see your docgrok
documentation in the docgrok browser.

Basically, the DocGrok should provide and extract all information
available for the kind of thing (a class, a function or whatever), you
want to document. The handler class determines, whether a special
dotted path denotes one of the things you want to document while the
docgrok view finally renders all this (hopefully) nicer than it is
done below.

The *DocGrok* classes should be derived from
grok.admin.docgrok.DocGrok, so that they automatically provide some
useful information like the Python path of an object and similar.

The *DocGrokHandlers* should be derived from
grok.admin.docgrok.DocGrokHandler to be registered automatically on
startup. It must provide a method ``getDoctor(dotted_path,
obj=None)``, which returns a DocGrok object iff the given dotted_path
denotes a thing of the appropriate type. In the example below we
check, whether a given dotted path denotes a Mammoth class and in
this case return a ``DocGrokForMammoths`` instance.

The *DocGrokView* finally renders the information of the DocGrok
instance, which is created, when a user requests information about a
certain MammothManager.

Example:
--------

We created the wonderfull Mammoth as below. Normally, when we watch
the docgrok documentation of that class, we would be served the usual
class documentation. But we want to give hints, that mammoths are
really _large_, so we have to provide a special docgrok.

All three of the above mentioned parts are defined below: a docgrok
only for the Mammoth class (and its subclasses), a docgrok handler,
which finds out, whether something is a Mammoth class and a view to
display some valuable information about mammoths.

Both, the handler and the view are registered automatically on
startup, because they are subclassing DocGrokHandler (the handler) and
grok.View (the view). There is nothing else, we have to do.

To check this, we have a look at the docgrok class browser. First we
have a look at the module, the class is contained in::

  >>> browser.open("http://localhost/docgrok/grok/ftests/admin/docgrok")

In this page, there should be a link available to our Mammoth class,
as defined below::

  >>> link = browser.getLink(url='/Mammoth')
  >>> link.text
  'Mammoth'

  >>> link.url
  'http://localhost/docgrok/grok/ftests/admin/docgrok/Mammoth'
  
If we click on this link, we normally would get a usual class
documentation page as generated by the docgrok for classes. But, while
we have registered a special docgrok for Mammoth-things, we get::

  >>> link.click()
  >>> print browser.contents
  An enormous beast.
  Mammoths are really tall.
  The size is: remarkable


"""
import grok
from grok.admin.docgrok import DocGrok, DocGrokHandler
from grok.admin.view import DocGrokView

class Mammoth(object):
    """A (large) thing, we want to document later on.
    """
    pass

class DocGrokForMammoths(DocGrok):
    """Documentation for Mammoths.
    """
    def getSize(self):
        return u"remarkable"

class DocGrokForMammothsHandler(DocGrokHandler):
    """A class for determining, whether a dotted path denotes a
    Mammoth.
    """
    def getDoctor(self, dotted_path, ob=None):
        """The only method required from a docgrok handler.
        """
        from zope.dottedname.resolve import resolve
        try:
            ob = resolve(dotted_path)
        except ImportError:
            return
        try:
            if not issubclass(ob, Mammoth):
                return
        except TypeError:
            return
        return DocGrokForMammoths(dotted_path)

class DocGrokViewForMammoths(grok.View):
    """A view, that should fit into the other docgrok documentation.
    """
    # We bind to the docgrok which provides us with information about
    # the thing, we want to document.
    grok.context(DocGrokForMammoths)
    grok.name('index')
    
    def render(self):
        """To avoid an extra template, we provide a render method.
        """
        return (u"An enormous beast.\n"
                u"Mammoths are really tall.\n"
                u"The size is: %s " % self.context.getSize())

