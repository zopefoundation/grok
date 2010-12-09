"""
Default Group Behaviour
-----------------------

Grok provides a default security policy.
Here we proofe that the basic stuff will work
as expected.

Note we defined the user and the permission in the ftesting.zcml

  >>> from zope.app.wsgi.testlayer import Browser
  >>> browser = Browser()

If we try to acces a public site without authentication
we will get the following goups 'zope.Anybody' and 'zope
Everybody'

  >>> browser.open("http://localhost/@@publicview")
  >>> 'zope.Anybody' in browser.contents
  True
  >>> 'zope.Everybody' in browser.contents
  True

If we try to acces a protect view by an anonyoums user
we will get an Unauthorized Message.

  >>> browser.open("http://localhost/@@protectedview")
  Traceback (most recent call last):
  ...
  HTTPError: HTTP Error 401: Unauthorized

If access the view with an authenticated request we should
get the groups zope.Authenticated.

  >>> browser.addHeader('Authorization', 'Basic foo:secret')
  >>> browser.open("http://localhost/@@publicview")
  >>> 'zope.Authenticated' in browser.contents
  True

And of course you can access the protected view.

  >>> browser.open("http://localhost/@@protectedview")
  >>> 'zope.Authenticated' in browser.contents
  True
"""

import grok
import zope.interface


class PublicView(grok.View):

    grok.context(zope.interface.Interface)
    grok.require('zope.Public')

    def render(self):
        return ', '.join(self.request.principal.groups)


class ProtectedView(grok.View):
    grok.context(zope.interface.Interface)
    grok.require('grok.test')

    def render(self):
        return ', '.join(self.request.principal.groups)
