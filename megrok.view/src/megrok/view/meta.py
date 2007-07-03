import zope.component
import zope.interface
from zope.publisher.interfaces.browser import IBrowserRequest

from z3c.template.template import TemplateFactory

import martian
from martian.error import GrokError
from martian import util

import grok
from grok.util import get_default_permission, make_checker

import megrok.view

class ViewGrokkerBase(martian.ClassGrokker):
    """Code resuse for View, ContentProvider and Viewlet grokkers"""
    component_class = None
    factory_name = ''
    view_name = ''
    layer_name = ''
    view_context = None

    def grok(self, name, factory, context, module_info, templates):
        self.view_context = util.determine_class_context(factory, context)
        factory.module_info = module_info
        self.factory_name = factory.__name__.lower()

        self.view_layer = util.class_annotation(factory, 'megrok.layer.layer',
                                           None) or module_info.getAnnotation('megrok.layer.layer',
                                               None) or IBrowserRequest

        self.view_name = util.class_annotation(factory, 'grok.name',
                                          self.factory_name)

        # find templates
        template_name = util.class_annotation(factory, 'grok.template',
                                              self.factory_name)
        template = templates.get(template_name)

        factory.template_name = template_name
        if self.factory_name != template_name:
            # grok.template is being used
            if templates.get(self.factory_name):
                raise GrokError("Multiple possible templates for view %r. It "
                                "uses grok.template('%s'), but there is also "
                                "a template called '%s'."
                                % (factory, template_name, self.factory_name),
                                factory)

        self.register_template(factory, template, template_name, templates)

        # __view_name__ is needed to support IAbsoluteURL on views
        factory.__view_name__ = self.view_name

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

    def register_template(self, factory, template, template_name, templates):
        """Jumping a bit here to make the z3c.template Macro available to the
        template, either it needs to be in grok.PageTemplate ...?"""

        print '\ntemplatename:', template_name,'template:', template,'factory:', factory, '\n'
        if template:
            templates.markAssociated(template_name)
            factory.template = template
        else:
            # we assume that a template has or will be grokked from a class
            pass


    def register(self, factory, module_info):
        """Must be defined in subclasses"""
        pass


class ViewGrokker(ViewGrokkerBase):
    component_class = megrok.view.View

    def register(self, factory, module_info):

        zope.component.provideAdapter(factory,
                                 adapts=(self.view_context, self.view_layer),
                                 provides=zope.interface.Interface,
                                 name=self.view_name)

class TemplateViewGrokker(ViewGrokkerBase):
    component_class = megrok.view.TemplateView

    def register(self, factory, module_info):

        zope.component.provideAdapter(factory,
                                 adapts=(self.view_context, self.view_layer),
                                 provides=zope.interface.Interface,
                                 name=self.view_name)

class LayoutViewGrokker(ViewGrokkerBase):
    component_class = megrok.view.LayoutView

    def register(self, factory, module_info):

        zope.component.provideAdapter(factory,
                                 adapts=(self.view_context, self.view_layer),
                                 provides=zope.interface.Interface,
                                 name=self.view_name)

    def register_template(self, factory, template, template_name, templates):
        """Jumping a bit here to make the z3c.template Macro available to the
        template, either it needs to be in grok.PageTemplate ...?"""
        contentType = getattr(factory, 'contentType', 'text/html')
        if template:
            templates.markAssociated(template_name)
            template = TemplateFactory(template.filename, contentType)
            factory.template = template
        else:
            # we assume that a template has or will be grokked from a class
            pass
        # also for the layout template
        layout_name = util.class_annotation(factory, 'megrok.view.layout', u'')
        layout = templates.get(layout_name)
        if layout:
            templates.markAssociated(layout_name)
            layout = TemplateFactory(layout.filename, contentType)
            factory.layout = layout
        else:
            # we assume that a template has or will be grokked from a class
            pass
            pass
