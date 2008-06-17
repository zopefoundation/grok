"""

==================
Test viewlet order
==================

If one wants the viewlets rendered in a certain order it's possible
to use the grok.order() directive.

Set up a content object in the application root::

  >>> root = getRootFolder()
  >>> root['fred'] = Fred()

Traverse to the view on the model object. We get the viewlets
registered for the default layer, with the anybody permission::

  >>> from zope.testbrowser.testing import Browser
  >>> browser = Browser()
  >>> browser.handleErrors = False
  >>> browser.open("http://localhost/fred/@@orderview")
  >>> print browser.contents
  Gold
  Bone
  Fred
  Cave
  Wilma
  Barney
  <BLANKLINE>

A different way of determining viewlet order is for the
viewletmanager to override the sort() method::

  >>> from zope.testbrowser.testing import Browser
  >>> browser = Browser()
  >>> browser.handleErrors = False
  >>> browser.open("http://localhost/fred/@@orderview2")
  >>> print browser.contents
  Cave
  Barney
  <BLANKLINE>

"""

import grok

class Fred(grok.Model):
    pass

class OrderView(grok.View):
    pass

class CaveManager(grok.ViewletManager):
    grok.view(OrderView)
    grok.name('cave')

class CaveViewlet(grok.Viewlet):
    grok.order(30)
    grok.viewletmanager(CaveManager)

    def render(self):
        return "Cave"

class BarneyViewlet(grok.Viewlet):
    grok.order(60)
    grok.viewletmanager(CaveManager)

    def render(self):
        return "Barney"

class BoneViewlet(grok.Viewlet):
    grok.order(10)
    grok.viewletmanager(CaveManager)

    def render(self):
        return "Bone"

class WilmaViewlet(grok.Viewlet):
    grok.order(50)
    grok.viewletmanager(CaveManager)

    def render(self):
        return "Wilma"

class GoldViewlet(grok.Viewlet):
    grok.order(1)
    grok.viewletmanager(CaveManager)

    def render(self):
        return "Gold"

class FredViewlet(grok.Viewlet):
    grok.order(20)
    grok.viewletmanager(CaveManager)

    def render(self):
        return "Fred"

class OrderView2(grok.View):
    grok.template('orderview')

class CaveManager2(grok.ViewletManager):
    grok.view(OrderView2)
    grok.name('cave')

    def sort(self, viewlets):
        # Alphabetical-by-name, reversed.
        return sorted(viewlets, reverse=True)

class NoExplicitOrderCaveViewlet(grok.Viewlet):
    grok.name('cave')
    grok.viewletmanager(CaveManager2)

    def render(self):
        return "Cave"

class NoExplicitOrderBarneyViewlet(grok.Viewlet):
    grok.name('barney')
    grok.viewletmanager(CaveManager2)

    def render(self):
        return "Barney"
