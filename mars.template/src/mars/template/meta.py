import os

import zope.component
import zope.interface
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.pagetemplate.interfaces import IPageTemplate

from z3c.template.template import TemplateFactory
from z3c.template.interfaces import ILayoutTemplate

import martian
from martian import util
from martian.error import GrokError

import grok
from grok.util import check_adapts

import mars.template

# TODO raise errors if anything missing?
class TemplateFactoryGrokkerBase(martian.ClassGrokker):
    component_class = None

    def grok(self, name, factory, context, module_info, templates):
        view_context = util.determine_class_context(factory, context)
        factory.module_info = module_info
        factory_name = factory.__name__.lower()

        template_name = util.class_annotation(factory, 'grok.template',
                                              factory_name)
        template = templates.get(template_name)
        if not template:
            raise GrokError("No template found for %r. Please define a template"
                                "to use."
                                % (factory),
                                factory)
        if factory_name != template_name:
            # grok.template is being used
            if templates.get(factory_name):
                raise GrokError("Multiple possible templates for template %r. It "
                                "uses grok.template('%s'), but there is also "
                                "a template called '%s'."
                                % (factory, template_name, factory_name),
                                factory)

        provides = util.class_annotation(factory, 'grok.provides', self.provides)
        macro = util.class_annotation(factory, 'mars.template.macro', None)
        contentType = util.class_annotation(factory,
                                    'mars.template.content_type', 'text/html')
        view_layer = util.class_annotation(factory, 'mars.layer.layer',
                                       None) or module_info.getAnnotation('mars.layer.layer',
                                       None) or IBrowserRequest
        view_name = util.class_annotation(factory, 'grok.name', '')


        filename = template.__grok_location__
        if not os.path.exists(filename):
            raise GrokError("Inline templates are not supported for %s."
                                " Please drop a tempate named %s in %s_templates."
                                % (factory.__name__, factory_name, factory.module_info.name),
                                factory)
        factory = TemplateFactory(filename, contentType, macro)
        templates.markAssociated(template_name)
        zope.interface.directlyProvides(factory, provides)
        print '\nname:', view_name,'context:', view_context,'factory:', factory, '\n'
        zope.component.provideAdapter(factory,
                                 adapts=(view_context, view_layer),
                                 provides=provides,
                                 name=view_name)
        return True


class TemplateFactoryGrokker(TemplateFactoryGrokkerBase):
    component_class = mars.template.TemplateFactory

    @property
    def provides(self):
        return IPageTemplate

class LayoutFactoryGrokker(TemplateFactoryGrokkerBase):
    component_class = mars.template.LayoutFactory

    @property
    def provides(self):
        return ILayoutTemplate


