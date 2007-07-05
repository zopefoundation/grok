import zope.component
import zope.interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer

from z3c.template.template import TemplateFactory

import martian
from martian.error import GrokError
from martian import util

import grok
from grok.util import get_default_permission, make_checker

import mars.view

class ViewGrokkerBase(martian.ClassGrokker):
    """Code resuse for View, ContentProvider and Viewlet grokkers"""
    component_class = None
    factory_name = ''
    view_name = ''
    layer_name = ''
    view_context = None
    provider = zope.interface.Interface

    def grok(self, name, factory, context, module_info, templates):
        self.view_context = util.determine_class_context(factory, context)
        factory.module_info = module_info
        self.factory_name = factory.__name__.lower()

        self.view_layer = util.class_annotation(factory, 'mars.layer.layer',
                                           None) or module_info.getAnnotation('mars.layer.layer',
                                               None) or IDefaultBrowserLayer

        self.view_name = util.class_annotation(factory, 'grok.name',
                                          self.factory_name)

        # is name defined for template?
        # if defined a named template is looked up
        factory._template_name = util.class_annotation(factory, 'grok.template', '')

        # __view_name__ is needed to support IAbsoluteURL on views
        # TODO check how this is working for these views
        factory.__view_name__ = self.view_name

        # don't know if this would ever need to be set
        self.provides = util.class_annotation(factory, 'grok.provides',
                                                self.provider)
        #print '\nname:', self.view_name,'context:', self.view_context,'factory:', factory,\
        #      'layer:', self.view_layer, '\n'
        self.register(factory, module_info)

        # protect view, public by default
        default_permission = get_default_permission(factory)
        make_checker(factory, factory, default_permission)

        # safety belt: make sure that the programmer didn't use
        # @grok.require on any of the view's methods.
        methods = util.methods_from_class(factory)
        for method in methods:
            if getattr(method, '__grok_require__', None) is not None:
                raise GrokError('The @grok.require decorator is used for '
                                'method %r in view %r. It may only be used '
                                'for XML-RPC methods.'
                                % (method.__name__, factory), factory)

        return True

    def register(self, factory, module_info):
        """Must be defined in subclasses, module_info may be necessary for further lookups"""
        pass


class TemplateViewGrokker(ViewGrokkerBase):
    component_class = mars.view.TemplateView

    def register(self, factory, module_info):

        zope.component.provideAdapter(factory,
                                 adapts=(self.view_context, self.view_layer),
                                 provides=self.provides,
                                 name=self.view_name)

class LayoutViewGrokker(ViewGrokkerBase):
    component_class = mars.view.LayoutView

    def register(self, factory, module_info):

        # is name defined for layout?
        # if defined a named template is looked up
        factory._layout_name = util.class_annotation(factory, 'mars.view.layout', '')

        zope.component.provideAdapter(factory,
                                 adapts=(self.view_context, self.view_layer),
                                 provides=self.provides,
                                 name=self.view_name)

