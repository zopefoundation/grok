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

  >>> import grok
  >>> grok.grok('grok.ftests.admin.loginlogout')

First setup the pluggable authentication system for session based
authentication. This is normaly invoked by an event
handler. Unfortunately the event handler seems not to be called, if
the ftesting setup is set up. We therefore set up the PAU manually.

  >>> root = getRootFolder()
  >>> root is not None
  True

  >>> import grok.admin
  >>> principal_credentials = grok.admin.getPrincipalCredentialsFromZCML()
  >>> principal_credentials
  [{u'login': u'mgr', u'password': u'mgrpw', u'id': u'zope.mgr', u'title': u'Manager'}]

  >>> grok.admin.setupSessionAuthentication(root_folder = root, principal_credentials = principal_credentials)

We should get a login page if trying to get something unauthenticated.

  >>> from zope.testbrowser.testing import Browser
  >>> browser = Browser()
  >>> browser.handleErrors = True
  >>> browser.open("http://localhost/")

  >>> print browser.contents
  <html xmlns="http://www.w3.org/1999/xhtml">
  ... <title>Grok Login</title>
  ...

Now try to log in using *wrong* credentials

  >>> browser.getControl(name='login').value = 'dumbtry'
  >>> browser.getControl('Login').click()
  >>> print browser.contents
  <html xmlns="http://www.w3.org/1999/xhtml">
  ... <title>Grok Login</title>
  ...

Okay, we got the login screen again. What about the correct credentials?

  >>> browser.getControl(name='login').value = 'mgr'
  >>> browser.getControl(name='password').value = 'mgrpw'
  >>> browser.getControl('Login').click()
  >>> print browser.contents
  <html xmlns="http://www.w3.org/1999/xhtml">
  ... <title>grok administration interface</title>
  ...

The new screen should contain a link for logging out:

  >>> print browser.contents
  <html xmlns="http://www.w3.org/1999/xhtml">
  ... <span>User:
  ...Manager
  ...[<a href="http://localhost/logout">log out</a>]
  ...
  
Fine. Now we are authorized and can do, whatever we want. Let's log out:

  >>> outlink = browser.getLink('log out')
  >>> outlink
  <Link text='log out' url='http://localhost/logout'>

  >>> outlink.click()
  >>> print browser.contents
  <html>
  ... You have been logged out.
  ...

Looks okay. But are we really logged out? Let's try to fetch a page:

  >>> browser.open("http://localhost/")
  >>> print browser.contents
  <html xmlns="http://www.w3.org/1999/xhtml">
  ... <title>Grok Login</title>
  ...
  ... <td><input id="login" type="text" name="login" /></td>
  ...

Yes, we are.

  ...
  ...      <legend>Add application</legend>
  ...


"""

