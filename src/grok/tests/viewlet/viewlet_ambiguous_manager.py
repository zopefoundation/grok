"""
When there are two or more viewletmanagers available in the module,
a viewlet will not auto-associate but instead raise an error.

  >>> grok.testing.grok(__name__)
  Traceback (most recent call last):
    ...
  GrokError: Multiple possible viewletmanagers for
  <class 'grok.tests.viewlet.viewlet_ambiguous_manager.Viewlet'>, please use
  the 'viewletmanager' directive.

"""

import grok
from zope.interface import Interface

class ViewletManager(grok.ViewletManager):
    grok.name('foo')
    grok.context(Interface)

class ViewletManager2(grok.ViewletManager):
    grok.name('bar')
    grok.context(Interface)

class Viewlet(grok.Viewlet):
    grok.context(Interface)

    def render(self):
        return "Render method"


