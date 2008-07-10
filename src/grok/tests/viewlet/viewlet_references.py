"""
A grok.ViewletManager instance has references to the components it was
registered for::

  >>> grok.testing.grok(__name__)
  >>> from zope import component
  >>> from zope.contentprovider.interfaces import IContentProvider
  >>> from zope.publisher.browser import TestRequest
  >>> ctxt = AContext()
  >>> request = TestRequest()
  >>> view = component.getMultiAdapter((ctxt, request), name='with_items')
  >>> items_mgr = component.getMultiAdapter(
  ...     (ctxt, request, view), IContentProvider, name='view_items_manager')
  >>> items_mgr.context is ctxt
  True
  >>> items_mgr.view is view
  True
  >>> items_mgr.request is request
  True

Likewise, grok.Viewlet instances have references to the components they're
registered for::

  >>> items_mgr.update()
  >>> for viewlet in items_mgr.viewlets:
  ...     viewlet.context is ctxt
  ...     viewlet.view is view
  ...     viewlet.viewletmanager is items_mgr
  ...     viewlet.request is request
  True
  True
  True
  True
  True
  True
  True
  True
"""

import grok
from zope import interface

class AContext(grok.Model):
    pass

class ViewWithItems(grok.View):
    grok.name('with_items')

    def render(self):
        return ''

class ViewItemsManager(grok.ViewletManager):
    grok.name('view_items_manager')

class ItemOneViewlet(grok.Viewlet):
    grok.name('item_one')

    def render(self):
        return "Item one reporting, sir!"

class ItemTwoViewlet(grok.Viewlet):
    grok.name('item_two')

    def render(self):
        return "Item two reporting, sir!"
