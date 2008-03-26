"""
We check whether viewlets automatically associate with templates in the
templates directory (viewlet_template_templates).

Set up the model object to view::

  >>> root = getRootFolder()
  >>> root['cave'] = Cave()

Viewing the cave object should result in the viewlet being displayed::

  >>> from zope.testbrowser.testing import Browser
  >>> browser = Browser()
  >>> browser.handleErrors = False
  >>> browser.open("http://localhost/cave")
  >>> print browser.contents
  <p>Hi, this is the fred viewlet speaking</p>

"""
import grok

class CavemenViewletManager(grok.ViewletManager):
    grok.name('manage.cavemen')

class FredViewlet(grok.Viewlet):
    grok.viewletmanager(CavemenViewletManager)

class Cave(grok.Model):
    pass

class Index(grok.View):
    pass
