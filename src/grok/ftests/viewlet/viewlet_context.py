"""
Viewlets and viewlet managers auto-associate with the context object that
may be in a module.

Set up the model object to view::

  >>> root = getRootFolder()
  >>> root['cave'] = cave = Cave()

We also set up another model that the viewlet manager and viewlets should
not be associated with::

  >>> from viewlet_context2 import Club
  >>> root['club'] = club = Club()

Let's get a viewletmanager associated with ``cave``::

  >>> from zope.publisher.browser import TestRequest
  >>> request = TestRequest()
  >>> from zope import component
  >>> view = component.getMultiAdapter((cave, request), name='index')
  >>> from zope.contentprovider.interfaces import IContentProvider
  >>> mgr = component.getMultiAdapter((cave, request, view), IContentProvider,
  ...   'manage.cavemen')
  
We cannot get this viewletmanager for ``club``, as there is no viewlet
manager associated with that as a context::

  >>> component.queryMultiAdapter((club, request, view), IContentProvider,
  ...   'manage.caveman') is None
  True

We can get the viewlet for ``cave``::
  
  >>> mgr['fredviewlet']
  <grok.ftests.viewlet.viewlet_context.FredViewlet object at ...>

We can also directly look it up using a manual lookup::

  >>> from zope.viewlet.interfaces import IViewlet
  >>> viewlet = component.getMultiAdapter((cave, request, view, mgr),
  ...   IViewlet, name='fredviewlet')

We cannot get the viewlet for the ``club`` however, as it is not associated
with the same context::

  >>> viewlet = component.getMultiAdapter((club, request, view, mgr),
  ...   IViewlet, name='fredviewlet')
  Traceback (most recent call last):
    ...
  ComponentLookupError: ...

"""

import grok
from zope.interface import Interface

class CavemenViewletManager(grok.ViewletManager):
    grok.name('manage.cavemen')

class FredViewlet(grok.Viewlet):
    grok.viewletmanager(CavemenViewletManager)

    def render(self):
        return 'Me Fred'

class Cave(grok.Model):
    pass

class Index(grok.View):
    def render(self):
        return "hoi"
