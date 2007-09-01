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

  >>> from zope.testbrowser.testing import Browser
  >>> browser = Browser()
  >>> browser.addHeader('Authorization', 'Basic mgr:mgrpw')
  
We fetch the documentation page, which should give us a tiny overview
over documentation:

  >>> browser.open("http://localhost/docgrok")
  >>> print browser.contents
  <html xmlns="http://www.w3.org/1999/xhtml">
  ...
  ... Welcome to DocGrok...
  ...

On the documentation page there should be a link to the ZODB root
folder:

  >>> root_link = browser.getLink('ZODB root folder')
  >>> root_link
  <Link text='ZODB root folder' url='http://localhost/@@inspect.html'>

The root folder got no name:

  >>> root_link.click()
  >>> print browser.contents
  <html xmlns="http://www.w3.org/1999/xhtml">
  ...
  ... <span>&lt;unnamed object&gt;</span>
  ...

and is of type Folder.

  >>> print browser.contents
  <html xmlns="http://www.w3.org/1999/xhtml">
  ...
  ... <span ...>...<a ...>Folder</a> object at ...&gt;</span>
  ...

It's class documentation should be linked in the head of page:

  >>> browser.getLink('Folder').url
  'http://localhost/docgrok/zope/app/folder/folder/Folder/'

We also get the docstring of the root folder:

  >>> print browser.contents
  <html xmlns="http://www.w3.org/1999/xhtml">
  ...
  ...<p>The standard Zope Folder implementation.</p>
  ...
  
A checkbox gives us control over private members and attributes of the
object displayed:

  >>> checkbox = browser.getControl('Show private attributes')
  >>> checkbox
  <ItemControl name='show_private' type='checkbox' optionValue='on' selected=False>

By default the checkbox is not selected. Therefore we check for an
arbitrary private method to be displayed or not. For example the
``__dict__`` method. By default no __dict__ method will be displayed:

  >>> '__dict__' in browser.contents
  False

Now let's tick the checkbox and update the view:

  >>> checkbox.selected = True
  >>> checkbox.selected
  True

  >>> browser.getControl('update').click()

Now the private method should be displayed:

  >>> '__dict__' in browser.contents
  True

Here we go :-)

Okay, now let's examine the displayed data a bit. We are currently the
object browser's view for the root folder. The root folder got no
parent, which should be displayed:

  >>> 'No parent object' in browser.contents
  True

One of the base classes of the root folder is the class
``persistent.Persistent``. We not only want that displayed but also a
link to the class documentation of that class:

  >>> link = browser.getLink("Persistent'")
  >>> link.url
  'http://localhost/docgrok/persistent/Persistent'

The same for interfaces. The root folder implements
``persistent.interfaces.IPersistent``:w

  >>> link = browser.getLink('IPersistent')
  >>> link.url
  'http://localhost/docgrok/persistent/interfaces/IPersistent/'

Now the attributes and properties. The root folder got an attribute
``data``:

  >>> print browser.contents
  <html xmlns="http://www.w3.org/1999/xhtml">
  ...
  ...<h3 ...>
  ...Attributes
  ...</h3>
  ... <span>data</span>
  ... <div>
  ...  value:
  ...   <a href="http://localhost/docgrok-obj/data/@@inspect.html">&lt;BTrees.OOBTree.OOBTree object at ...&gt;</a>
  ... </div>
  ...
  


"""
