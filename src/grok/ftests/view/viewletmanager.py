"""
  >>> import grok
  >>> from grok.ftests.view.viewletmanager import Mammoth
  >>> grok.grok('grok.ftests.view.viewletmanager')
  >>> getRootFolder()["manfred"] = Mammoth()

  >>> from zope.testbrowser.testing import Browser
  >>> browser = Browser()
  >>> browser.handleErrors = False
  >>> browser.open("http://localhost/++skin++myskin/manfred/@@painting")
  >>> print browser.contents
  <html>
  <body>
  <h1>This is a cave painting</h1>
  <div><p>Hello World</p></div>
  </body>
  </html>

"""
import grok

from zope.publisher.interfaces.browser import IBrowserRequest, IBrowserView
from zope.contentprovider.interfaces import IContentProvider
from zope.viewlet.interfaces import IViewletManager
from zope.viewlet.interfaces import IViewlet
from zope.viewlet.viewlet import ViewletBase
import zope.component

from z3c.viewlet.manager import WeightOrderedViewletManager

class Mammoth(grok.Model):
    pass

class IMySkinLayer(grok.ILayer):
    pass

class MySkin(grok.Skin):
    grok.layer(IMySkinLayer)

class Painting(grok.View):
    """Template must be in *_templates, I tried and I tried to find out
    why when inline the `provider` tal directive wasn't found"""
    pass

class MammothContentProvider(grok.MultiAdapter):
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

class MammothViewletManager(grok.MultiAdapter, WeightOrderedViewletManager):
    grok.adapts(Mammoth, IMySkinLayer, IBrowserView)
    grok.name('cavecolumn')

    def __init__(self, context, request, view):
        WeightOrderedViewletManager.__init__(self, context, request, view)

    def update(self):
        viewlets = zope.component.getAdapters(
                    (self.context, self.request, self.__parent__, self),
                    IViewlet)
        self.viewlets = []
        for viewlet in viewlets:
            self.viewlets.append(viewlet[1])

    def render(self):
        return '\n'.join([s.render() for s in self.viewlets])

class HelloWorldViewlet(grok.MultiAdapter):
    grok.adapts(Mammoth, IMySkinLayer, IBrowserView, IViewletManager)
    grok.implements(IViewlet)
    grok.name('helloworld')
    weight = 0

    def __init__(self, context, request, view, manager):
        self.__parent__ = view
        self.context = context
        self.request = request
        self.manager = manager

    def render(self):
        return u'<p>Hello World</p>'

class FirstProvider(grok.ContentProvider):
    grok.name('provider.first')
    grok.context(Mammoth)

    def update(self):
        pass
