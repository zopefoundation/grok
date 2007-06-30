"""
  >>> import grok
  >>> from grok.ftests.view.provider import Mammoth
  >>> grok.grok('grok.ftests.view.provider')
  >>> getRootFolder()["manfred"] = Mammoth()

  >>> from zope.testbrowser.testing import Browser
  >>> browser = Browser()
  >>> browser.handleErrors = False
  >>> browser.open("http://localhost/++skin++myskin/manfred/@@painting")
  >>> print browser.contents
  <html>
  <body>
  <h1>This is a cave painting</h1>
  </body>
  </html>

"""
import grok

from zope.publisher.interfaces.browser import IBrowserRequest, IBrowserView
from zope.contentprovider.interfaces import IContentProvider


class Mammoth(grok.Model):
    pass

class IMySkinLayer(grok.ILayer):
    pass

class MySkin(grok.Skin):
    grok.layer(IMySkinLayer)

class Painting(grok.View):
    pass

class MammothContentProvider(grok.MultiAdapter, ):
    grok.adapts(Mammoth, IMySkinLayer, IBrowserView)
    grok.implements(IContentProvider)
    grok.name('cave')

    def __init__(self, context, request, view):
        self.context = context
        self.request = request
        self.view = self.__parent__ = view

    def update(self):
        pass

    def render(self):
        return u'This is a cave painting'

