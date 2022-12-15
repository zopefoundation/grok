"""

Permissions already set by non-grok components are preserved by the
Grok publisher.

Let's first define a ``@@contents.html`` that is protected by a Zope
permission, ``zope.ManageContent``::

  >>> from zope.publisher.browser import BrowserPage
  >>> from zope.testbrowser.wsgi import Browser
  >>> class Contents(BrowserPage):
  ...   def __init__(self, context, request):
  ...     self.context = context
  ...     self.request = request
  ...   def __call__(self):
  ...     return "Contents called"
  >>> from zope import component
  >>> from zope.interface import Interface
  >>> from zope.publisher.interfaces.browser import IBrowserRequest
  >>> component.provideAdapter(Contents,
  ...   adapts=(Interface, IBrowserRequest),
  ...   provides=Interface,
  ...   name='contents.html')
  >>> from zope.security.checker import Checker, defineChecker
  >>> required = {}
  >>> required['__call__'] = 'zope.ManageContent'
  >>> required['browserDefault'] = 'zope.ManageContent'
  >>> defineChecker(Contents, Checker(required))

The `@@contents.html` view of folders is protected by
`zope.ManageContent` and should not be visible to unauthenticated
users. Instead we are asked to authenticate ourselves::

  >>> print(str(http(
  ...     wsgi_app(), b'GET /@@contents.html HTTP/1.1', handle_errors=False)))
  Traceback (most recent call last):
  zope.security.interfaces.Unauthorized: ...

Let's test this in the context of a Grok application:

  >>> grok.testing.grok(__name__)
  >>> from grok.ftests.security.preserve_permissions import App
  >>> root = getRootFolder()
  >>> root['app'] = App()

Now there is a ``contents.html`` view available for our application,
which is protected by default::

  >>> print(str(http(
  ...     wsgi_app(),
  ...     b'GET /app/@@contents.html HTTP/1.1',
  ...     handle_errors=False)))
  Traceback (most recent call last):
  zope.security.interfaces.Unauthorized: ...

However, if we make a grant, e.g. on the root object, we can access
the view just fine:

  >>> from zope.securitypolicy.interfaces import IPrincipalPermissionManager
  >>> root = getRootFolder()
  >>> root_perms = IPrincipalPermissionManager(root)
  >>> root_perms.grantPermissionToPrincipal('zope.ManageContent',
  ...                                       'zope.anybody')
  >>> print(str(http(wsgi_app(), b'GET /@@contents.html HTTP/1.1')))
  HTTP/1.1 200 Ok
  ...

The default view is accessible::

  >>> browser = Browser()
  >>> browser.open('http://localhost/app')
  >>> print(browser.contents)
  Moo!

While the manage view is locked::

  >>> # Work around https://github.com/python/cpython/issues/90113
  >>> browser.raiseHttpErrors = False
  >>> browser.open('http://localhost/app/@@manage')
  >>> print(browser.headers['status'])
  401 Unauthorized

When we authenticate, everything works fine::

  >>> browser.addHeader('Authorization', 'Basic mgr:mgrpw')
  >>> browser.open('http://localhost/app/@@manage')
  >>> print(browser.contents)
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
