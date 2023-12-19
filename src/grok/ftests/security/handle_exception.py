"""
The handleException() method has a special case that might introduce a proxy
and cause the grok security to fail, we have a simple test here that assures
that we don't hit this:

  >>> from zope.testbrowser.wsgi import Browser
  >>> browser = Browser()
  >>> # Work around https://github.com/python/cpython/issues/90113
  >>> browser.raiseHttpErrors = False
  >>> browser.open("http://localhost/@@cave")
  >>> print(browser.headers['status'])
  500 Internal Server Error
  >>> browser.contents
  'It is gone!'

"""

from zope.interface import Interface

import grok


class CaveWasRobbedError(Exception):
    pass


class Cave(grok.View):
    """Home of Grok.
    """
    grok.context(Interface)

    fire = 'It is gone!'

    def render(self):
        raise CaveWasRobbedError("EVERYTHING GONE! GROK ANGRY!")


class CaveErrorView(grok.View):
    """Default view for the CaveWasRobbedError.
    """
    grok.name("index")
    grok.context(CaveWasRobbedError)

    def render(self):
        self.request.response.setStatus(500)
        return self.context.__parent__.fire
