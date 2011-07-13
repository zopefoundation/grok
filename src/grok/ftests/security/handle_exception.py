"""
The handleException() method has a special case that might introduce a proxy
and cause the grok security to fail, we have a simple test here that assures
that we don't hit this:

  >>> from zope.app.wsgi.testlayer import Browser
  >>> browser = Browser()
  >>> browser.open("http://localhost/@@cave")
  Traceback (most recent call last):
  HTTPError: HTTP Error 500: Internal Server Error
  >>> browser.contents
  'It is gone!'

"""

import grok
from zope.interface import Interface


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
