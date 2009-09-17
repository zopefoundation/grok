"""

When the publisher is called in ``handle_errors=False`` mode, as
happens when running Grok with paster and WSGI debugger middleware,
IUnauthorized exceptions are handled anyway by the publisher.

We create a simple site with a protected ``index`` view:

    >>> root = getRootFolder()
    >>> root['app'] = App()

When we call the protected view with ``handle_errors`` set to
``False``, we will get no exception but instead an HTTP error:

    >>> from zope.app.testing.functional import HTTPCaller
    >>> http_call = HTTPCaller()

    >>> print http_call("GET /app/@@index HTTP/1.1" + chr(13),
    ...                 handle_errors=False)
    HTTP/1.1 401 Unauthorized
    ...

"""
import grok

class ManagerPerm(grok.Permission):
    grok.name('grok.Manager')

class App(grok.Application, grok.Container):
    pass

class Index(grok.View):
    grok.require('grok.Manager')
    def render(self):
        return 'Hello from protected view'
