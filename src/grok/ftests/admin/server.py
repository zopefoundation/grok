##############################################################################
#
# Copyright (c) 2008 Zope Corporation and Contributors.
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
Tests for the server functionality of the admin interface.

We start with authenticating ourselves::

  >>> from zope.testbrowser.testing import Browser
  >>> browser = Browser()
  >>> browser.addHeader('Authorization', 'Basic mgr:mgrpw')
  
We fetch the standard page, which should provide us a menu to get all
installable grok applications/components::

  >>> browser.open("http://localhost/")
  >>> print browser.contents
  <html xmlns="http://www.w3.org/1999/xhtml">
  ...
  ...      <legend>Add application</legend>
  ...

There should be a link to the server admin pages::

  >>> print browser.contents
  <html xmlns="http://www.w3.org/1999/xhtml">
  ...
  ...   <a href="http://localhost/server">Server Control</a>
  ...

Now we can click that link and should get the server administration
page::

  >>> browser.getLink('Server Control').click()
  >>> browser.title
  'grok administration interface'

We can enter an admin message::

  >>> admin_msg_ctrl = browser.getControl(name='admin_message')
  >>> admin_msg_ctrl
  <Control name='admin_message' type='text'>

  >>> admin_msg_ctrl.value = 'Hi there!'

If we submit that message, it should appear in the page::

  >>> msg_form = browser.getForm(index=1)
  >>> msg_form.submit()
  >>> print browser.contents
  <html xmlns="http://www.w3.org/1999/xhtml">
  ... <li class="admin">Hi there!</li>
  ...

The message stays, even if we call another page::

  >>> browser.getLink('Applications').click()
  >>> print browser.contents
  <html xmlns="http://www.w3.org/1999/xhtml">
  ...
  ... <li class="admin">Hi there!</li>
  ...
  ...
  ...      <legend>Add application</legend>
  ...

Get back to the server stuff::

  >>> browser.getLink('Server Control').click()
  >>> print browser.contents
  <html xmlns="http://www.w3.org/1999/xhtml">
  ...
  ... <li class="admin">Hi there!</li>
  ...


"""
