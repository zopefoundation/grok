"""
This doctest uses grok.ContentProvider, megrok.view.ViewletManager and grok.Viewlet.

  >>> import grok
  >>> from megrok.viewlet.tests.viewlet.view import Mammoth
  >>> grok.grok('megrok.viewlet.tests.viewlet.view')
  >>> getRootFolder()["manfred"] = Mammoth()

  >>> from zope.testbrowser.testing import Browser
  >>> browser = Browser()
  >>> browser.handleErrors = False
  >>> browser.open("http://localhost/manfred/@@index")
  >>> print browser.contents
  <html>
  <body>
  <h1>Manfred</h1>
  <div id="leftcolumn">
  <p>My simple viewlet</p>
  <p>This is from a template for Manfred</p>
  </div>
  <div>Way cool</div>
  <div id="rightcolumn">
  </div>
  </body>
  </html>

  >>> browser.open("http://localhost/manfred/@@skinnedindex")
  Traceback (most recent call last):
  ...
  NotFound...'@@skinnedindex'

  >>> browser.open("http://localhost/++skin++myskin/manfred/@@skinnedindex")
  >>> print browser.contents
  <html>
  <body>
  <h1>Manfred</h1>
  <div id="leftcolumn">
  <p>My skinned viewlet</p>
  <p>My simple viewlet</p>
  <p>This is from a template for Manfred</p>
  </div>
  <div>Way cool</div>
  <div id="rightcolumn">
  </div>
  </body>
  </html>

"""
import grok
import megrok.layer
import megrok.viewlet
import megrok.view

class Mammoth(grok.Model):
    title = u'Manfred'

class IMySkinLayer(megrok.layer.IMinimalLayer):
    pass

class MySkin(megrok.layer.Skin):
    megrok.layer.layer(IMySkinLayer)

class Index(megrok.view.View):
    """Template must be in *_templates, I tried and I tried to find out
    why when the template is inline the `provider` tal directive isn't found"""
    pass

class SkinnedIndex(megrok.view.View):
    """Template must be in *_templates, I tried and I tried to find out
    why when the template is inline the `provider` tal directive isn't found"""
    megrok.layer.layer(IMySkinLayer)

class Title(megrok.viewlet.ContentProvider):
    """This has a template"""
    grok.name('site.title')
    grok.context(Mammoth)

class FirstManager(megrok.viewlet.ViewletManager):
    """This has a template also, ie it acts just like the above"""
    grok.name('site.firstmanager')
    grok.context(Mammoth)

class RightColumnManager(megrok.viewlet.ViewletManager):
    """This has no template and no viewlets, it renders nothing"""
    grok.name('site.rightcolumnmanager')
    grok.context(Mammoth)

class LeftColumnManager(megrok.viewlet.ViewletManager):
    """This has no template it renders its viewlets"""
    grok.name('site.leftcolumnmanager')
    grok.context(Mammoth)

class FirstViewlet(megrok.viewlet.Viewlet):
    """A simple viewlet"""
    grok.name('site.viewlet.simple')
    grok.context(Mammoth)
    megrok.viewlet.viewletmanager(LeftColumnManager)
    weight = 0

    def render(self):
        return u'<p>My simple viewlet</p>'

class SecondViewlet(megrok.viewlet.Viewlet):
    """A viewlet that has its own template"""
    grok.name('site.viewlet.templated')
    grok.context(Mammoth)
    megrok.viewlet.viewletmanager(LeftColumnManager)
    weight = 1

class ThirdViewlet(megrok.viewlet.Viewlet):
    """A simple viewlet for a specific layer only"""
    grok.name('site.viewlet.skinned')
    grok.context(Mammoth)
    megrok.viewlet.viewletmanager(LeftColumnManager)
    megrok.layer.layer(IMySkinLayer)
    weight = 0

    def render(self):
        return u'<p>My skinned viewlet</p>'


