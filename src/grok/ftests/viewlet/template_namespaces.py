"""

  >>> root = getRootFolder()
  >>> root['cave'] = Cave()
  >>> from zope.testbrowser.testing import Browser
  >>> browser = Browser()
  >>> browser.handleErrors = False
  >>> browser.open("http://localhost/cave/@@index")
  >>> print browser.contents
  <grok.ftests.viewlet.template_namespaces.Cave object at ...>
  <grok.ftests.viewlet.template_namespaces.Index object at ...>
  <grok.ftests.viewlet.template_namespaces.MirandaViewlet object at ...>
  <grok.ftests.viewlet.template_namespaces.CavewomenViewletManager object at ...>

  >>> browser.open("http://localhost/cave/@@necklace")
  >>> print browser.contents
  <grok.ftests.viewlet.template_namespaces.Cave object at ...>
  <grok.ftests.viewlet.template_namespaces.Necklace object at ...>
  <grok.ftests.viewlet.template_namespaces.CavewomenViewletManagerWithTemplate object at ...>

"""
import grok


class Cave(grok.Model):
    pass

class Index(grok.View):
    pass

class CavewomenViewletManager(grok.ViewletManager):
    grok.name('manage.cavewomen')
    grok.view(Index)

class MirandaViewlet(grok.Viewlet):
    grok.template('mirandaviewlet')
    grok.view(Index)
    grok.viewletmanager(CavewomenViewletManager)

class Necklace(grok.View):
    pass

class CavewomenViewletManagerWithTemplate(grok.ViewletManager):
    grok.name('manage.cavewomenwithtemplate')
    grok.template('mirandaviewletmanager')
    grok.view(Necklace)
