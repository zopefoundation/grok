"""
Viewing a protected view with insufficient privileges will yield
Unauthorized:

  >>> from zope.testbrowser.testing import Browser
  >>> browser = Browser()
  >>> browser.open("http://localhost/@@painting")
  Traceback (most recent call last):
  HTTPError: HTTP Error 401: Unauthorized

When we log in (e.g. as a manager), we can access the view just fine:

  >>> from zope.securitypolicy.rolepermission import rolePermissionManager
  >>> rolePermissionManager.grantPermissionToRole('cave.ViewPainting',
  ...                                             'zope.Manager')
  >>> browser.addHeader('Authorization', 'Basic mgr:mgrpw')
  >>> browser.handleErrors = False
  >>> browser.open("http://localhost/@@painting")
  >>> print browser.contents
  What a beautiful painting.

A view protected with 'zope.Public' is always accessible:

  >>> browser = Browser()
  >>> browser.open("http://localhost/@@publicnudity")
  >>> print browser.contents
  Everybody can see this.

To require permission one can refer either to the permission's id or the the
permission class too::

  >>> browser = Browser()
  >>> browser.open("http://localhost/@@profanity")
  Traceback (most recent call last):
  HTTPError: HTTP Error 401: Unauthorized

When we log in (e.g. as a manager), we can access the view just fine:

  >>> from zope.securitypolicy.rolepermission import rolePermissionManager
  >>> rolePermissionManager.grantPermissionToRole('cave.ViewPainting',
  ...                                             'zope.Manager')
  >>> browser.addHeader('Authorization', 'Basic mgr:mgrpw')
  >>> browser.handleErrors = False
  >>> browser.open("http://localhost/@@profanity")
  >>> print browser.contents
  Harsh words here.

"""

import grok
import zope.interface

class ViewPainting(grok.Permission):
    grok.name('cave.ViewPainting')

class Painting(grok.View):

    grok.context(zope.interface.Interface)
    grok.require(ViewPainting)

    def render(self):
        return 'What a beautiful painting.'

class PublicNudity(grok.View):

    grok.context(zope.interface.Interface)
    grok.require(grok.Public)

    def render(self):
        return 'Everybody can see this.'

class Profanity(grok.View):

    grok.context(zope.interface.Interface)
    grok.require(ViewPainting)

    def render(self):
        return 'Harsh words here.'
