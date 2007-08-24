"""

The handleException() method has a special case that might introduce a proxy
and cause the grok security to fail, we have a simple test here that assures
that we don't hit this:

  >>> from zope.testbrowser.testing import Browser
  >>> browser = Browser()
  >>> browser.open("http://localhost/@@cave")
  Traceback (most recent call last):
  HTTPError: HTTP Error 500: Internal Server Error
  >>> browser.contents
  "It's gone!"

"""

import zope.interface

import grok


class CaveWasRobbedError(Exception):
    pass


class Cave(grok.View):

    grok.context(zope.interface.Interface)

    fire = "It's gone!"

    def render(self):
        raise CaveWasRobbedError("EVERYTHING GONE! GROK ANGRY!")


class CaveErrorView(grok.View):

    grok.context(CaveWasRobbedError)
    grok.name("index.html")

    def render(self):
        self.request.response.setStatus(500)
        return self.context.__parent__.fire
