"""

Permissions already set by non-grok components are preserved by the
Grok publisher.

The `@@contents.html` view of folders is protected by
`zope.ManageContent` and should not be visible to unauthenticated
users. Instead we are asked to authenticate ourselves::

  >>> print http(r'''
  ... GET /@@contents.html HTTP/1.1
  ... ''')
  HTTP/1.1 401 Unauthorized
  ...
  WWW-Authenticate: basic realm="Zope"
  ...

This is also the case for views on the Grok application object::

  >>> grok.testing.grok(__name__)
  >>> from grok.ftests.security.preserve_permissions import App
  >>> root = getRootFolder()
  >>> root['app'] = App()
  >>> print http(r'''
  ... GET /app/++etc++site HTTP/1.1
  ... ''')
  HTTP/1.1 401 Unauthorized
  ...
  WWW-Authenticate: basic realm="Zope"
  ...

We can allow our application to be viewed by the Zope standard
``contents.html`` view for site folders. For this we make it provide
`ISiteManagementFolder`::

  >>> from zope.site.interfaces import ISiteManagementFolder
  >>> from zope.interface import alsoProvides
  >>> alsoProvides(root['app'], ISiteManagementFolder)

Now there is a ``contents.html`` view available for our application,
which is protected by default::

  >>> print http(r'''
  ... GET /app/@@contents.html HTTP/1.1
  ... ''')
  HTTP/1.1 401 Unauthorized
  ...
  
However, if we make a grant, e.g. on the root object, we can access
the view just fine:

  >>> from zope.securitypolicy.interfaces import IPrincipalPermissionManager
  >>> root = getRootFolder()
  >>> root_perms = IPrincipalPermissionManager(root)
  >>> root_perms.grantPermissionToPrincipal('zope.ManageContent',
  ...                                       'zope.anybody')
  >>> print http(r'''
  ... GET /@@contents.html HTTP/1.1
  ... ''')
  HTTP/1.1 200 Ok
  ...

The default view is accessible::
  
  >>> from zope.testbrowser.testing import Browser
  >>> browser = Browser()
  >>> browser.open('http://localhost/app')
  >>> print browser.contents
  Moo!

While the manage view is locked::

  >>> browser.open('http://localhost/app/@@manage')
  Traceback (most recent call last):
  ...
  httperror_seek_wrapper: HTTP Error 401: Unauthorized

We have some static resources defined in a local `static` directory,
which we can access unauthenticated::

  >>> browser.open('http://localhost/@@/grok.ftests.security/textfile.txt')
  >>> print browser.contents
  Just a test.

When we authenticate, everything works fine::

  >>> browser.addHeader('Authorization', 'Basic mgr:mgrpw')
  >>> browser.open('http://localhost/app/@@manage')
  >>> print browser.contents
  Woo!
  
"""
import grok

class ManageApp(grok.Permission):
    grok.name('app.Manage')

class App(grok.Application, grok.Container):
    pass

class Index(grok.View):
    def render(self):
        return 'Moo!'

class Manage(grok.View):
    grok.require('app.Manage')
    def render(self):
        return 'Woo!'
