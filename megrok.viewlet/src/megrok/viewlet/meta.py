import zope.component
from zope.publisher.interfaces.browser import (IBrowserRequest,
                                               IBrowserView)
from zope.viewlet.interfaces import IViewlet, IViewletManager
from zope.contentprovider.interfaces import IContentProvider

import martian
from martian import util
from martian.error import GrokError

import grok
from grok.util import get_default_permission, make_checker

import megrok.viewlet
from megrok.view.meta import ViewGrokkerBase

class ContentProviderGrokker(ViewGrokkerBase):
    """Also groks ViewletManager"""
    component_class = megrok.viewlet.ContentProvider

    def register(self, factory, module_info):

        if util.check_subclass(factory, megrok.viewlet.ViewletManager):
            view_provider = IViewletManager
        else:
            view_provider = IContentProvider
        zope.component.provideAdapter(factory,
                                 adapts=(self.view_context, self.view_layer, IBrowserView),
                                 provides=view_provider,
                                 name=self.view_name)


class ViewletGrokker(ViewGrokkerBase):
    component_class = megrok.viewlet.Viewlet

    def register(self, factory, module_info):

        view_manager = util.class_annotation(factory, 'megrok.viewlet.viewletmanager',
                                           None) or module_info.getAnnotation('megrok.viewlet.viewletmanager',
                                               None) or IViewletManager

        zope.component.provideAdapter(factory,
                                 adapts=(self.view_context, self.view_layer, 
                                         IBrowserView, view_manager),
                                 provides=IViewlet,
                                 name=self.view_name)

