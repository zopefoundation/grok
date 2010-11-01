"""
Non-grok views, that also provide `IGrokSecurityView` are handled more
openly by the Grok publisher.

We create an app, that provides a non-Grok view::

  >>> root = getRootFolder()
  >>> root['app'] = App()

The view must be registered first. We register it for our `app` as
context::

  >>> from zope.publisher.interfaces.browser import IDefaultBrowserLayer
  >>> from grok.ftests.security.security_view import App, Index

  >>> from zope.component import provideAdapter
  >>> from zope.interface import Interface
  >>> provideAdapter(Index, (App, IDefaultBrowserLayer), Interface, 'index')

We create a permission checker for this view, which allows everybody
to use the `__call__` method::

  >>> from grokcore.view import make_checker
  >>> make_checker(App, Index, None)

However, when we want to watch this view, we run into trouble::

  >>> from zope.app.wsgi.testlayer import Browser
  >>> browser = Browser()
  >>> browser.handleErrors = False
  >>> browser.open('http://localhost/app/@@index')
  Traceback (most recent call last):
  ...
  ForbiddenAttribute: ('browserDefault', <...Index object at 0x...>)

This happens, because we did not set any permissions for the
`browserDefault` method, which in 'normal' Zope3 environments means,
that access to this attribute/method is forbidden for unauthenticated
users.

Grok, however, provides a different security policy, which is less
strict in checking attribute and method permissions. This open policy
is for security reasons *not* applied to non-grok views, except, if
the view provides `IGrokSecurityView` and this way tells, that it
really wants the grok security to be applied on its methods and
attributes.

We let instances of `Index` provide `IGrokSecurityView`::

  >>> from zope.interface import classImplements
  >>> import grokcore.view
  >>> classImplements(Index, grokcore.view.IGrokSecurityView)

Now we can watch the view::

  >>> browser.open('http://localhost/app/@@index')
  >>> print browser.contents
  Hello from index

"""
import grok
from zope.publisher.browser import BrowserPage

class App(grok.Application, grok.Container):
    pass

class Index(BrowserPage):
    def __call__(self):
        return 'Hello from index'
