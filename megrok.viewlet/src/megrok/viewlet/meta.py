import martian
import grok
from zope import component
from zope.publisher.interfaces.browser import (IBrowserRequest,
                                               IBrowserView)
from zope.viewlet.interfaces import IViewlet, IViewletManager
from zope.contentprovider.interfaces import IContentProvider

from martian import util
import megrok.viewlet
from grok.util import get_default_permission, make_checker

class ViewGrokkerBase(martian.ClassGrokker):
    """Code resuse for View, ContentProvider and Viewlet grokkers"""
    component_class = None
    factory_name = ''
    view_context = None

    def grok_start(self, name, factory, context, module_info, templates):
        self.view_context = util.determine_class_context(factory, context)
        factory.module_info = module_info
        self.factory_name = factory.__name__.lower()

        # find templates
        template_name = util.class_annotation(factory, 'grok.template',
                                              self.factory_name)
        template = templates.get(template_name)

        if self.factory_name != template_name:
            # grok.template is being used
            if templates.get(self.factory_name):
                raise GrokError("Multiple possible templates for view %r. It "
                                "uses grok.template('%s'), but there is also "
                                "a template called '%s'."
                                % (factory, template_name, self.factory_name),
                                factory)

        if template:
            templates.markAssociated(template_name)
            factory.template = template
        else:
            if not getattr(factory, 'render', None):
                # we do not accept a view without any way to render it
                raise GrokError("View %r has no associated template or "
                                "'render' method." % factory, factory)

    def grok_end(self, factory):
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

class ContentProviderGrokker(ViewGrokkerBase):
    """Also groks ViewletManager"""
    component_class = megrok.viewlet.ContentProvider

    def grok(self, name, factory, context, module_info, templates):
        self.grok_start(name, factory, context, module_info, templates)

        view_layer = util.class_annotation(factory, 'megrok.layer.layer',
                                           None) or module_info.getAnnotation('megrok.layer.layer',
                                               None) or IBrowserRequest

        view_name = util.class_annotation(factory, 'grok.name',
                                          self.factory_name)
        # __view_name__ is needed to support IAbsoluteURL on views
        factory.__view_name__ = view_name
        if util.check_subclass(factory, megrok.viewlet.ViewletManager):
            view_provider = IViewletManager
        else:
            view_provider = IContentProvider
        component.provideAdapter(factory,
                                 adapts=(self.view_context, view_layer, IBrowserView),
                                 provides=view_provider,
                                 name=view_name)

        self.grok_end(factory)

        return True

class ViewletGrokker(ViewGrokkerBase):
    component_class = megrok.viewlet.Viewlet

    def grok(self, name, factory, context, module_info, templates):
        self.grok_start(name, factory, context, module_info, templates)

        view_layer = util.class_annotation(factory, 'megrok.layer.layer',
                                           None) or module_info.getAnnotation('megrok.layer.layer',
                                               None) or IBrowserRequest

        view_name = util.class_annotation(factory, 'grok.name',
                                          self.factory_name)
        view_manager = util.class_annotation(factory, 'megrok.viewlet.viewletmanager',
                                           None) or module_info.getAnnotation('megrok.viewlet.viewletmanager',
                                               None) or IViewletManager
        # __view_name__ is needed to support IAbsoluteURL on views
        factory.__view_name__ = view_name
        component.provideAdapter(factory,
                                 adapts=(self.view_context, view_layer, 
                                         IBrowserView, view_manager),
                                 provides=IViewlet,
                                 name=view_name)


        self.grok_end(factory)

        return True

