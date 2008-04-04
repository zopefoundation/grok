"""
=============================
Test viewletmanager templates
=============================

We want to show the usage of a template provided to the ViewletManager itself.
This ViewletManager also makes its viewlets accessible by their name.
Viewlets have a render method or a template attached.
The grok.order() directive is ignored in this context.

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
  <ul>
   <li>Barney</li>
   <li>Bone</li>
   <li>Cave</li>
   <li>Fred</li>
   <li>Gold</li>
   <li>Wilma</li>
  </ul>
  <BLANKLINE>
"""

import grok

class Fred(grok.Model):
    pass

class OrderView(grok.View):
    pass

class CaveManager(grok.ViewletManager):
    grok.name('cave')

    def viewlet_dict(self):
        v_dict={}
        for v in self.viewlets:
            v_dict[v.__name__]=v
        return v_dict

    def viewlet_keys_sorted(self):
        k=self.viewlet_dict().keys()
        k.sort()
        return k

class CaveViewlet(grok.Viewlet):
    grok.order(30)
    grok.viewletmanager(CaveManager)
    grok.name('Cave')

    def render(self):
        return "Cave"

class BarneyViewlet(grok.Viewlet):
    grok.order(60)
    grok.viewletmanager(CaveManager)
    grok.name('Barney')

class BoneViewlet(grok.Viewlet):
    grok.order(10)
    grok.viewletmanager(CaveManager)
    grok.name('Bone')

    def render(self):
        return "Bone"

class WilmaViewlet(grok.Viewlet):
    grok.order(50)
    grok.viewletmanager(CaveManager)
    grok.name('Wilma')

    def render(self):
        return "Wilma"

class GoldViewlet(grok.Viewlet):
    grok.order(1)
    grok.viewletmanager(CaveManager)
    grok.name('Gold')

    def render(self):
        return "Gold"

class FredViewlet(grok.Viewlet):
    grok.order(20)
    grok.viewletmanager(CaveManager)
    grok.name('Fred')

    def render(self):
        return "Fred"
