import zope.component
import zope.interface
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.pagetemplate.interfaces import IPageTemplate

from z3c.template.template import TemplateFactory

import martian
from martian import util

import grok
from grok.util import check_adapts

import megrok.template

# TODO raise errors if anything missing?
class TemplateFactoryGrokker(martian.ClassGrokker):
    component_class = megrok.template.TemplateFactory

    def grok(self, name, factory, context, module_info, templates):
        view_context = util.determine_class_context(factory, context)
        factory.module_info = module_info
        factory_name = factory.__name__.lower()

        template_name = util.class_annotation(factory, 'grok.template',
                                              factory_name)
        template = templates.get(template_name)
        if factory_name != template_name:
            # grok.template is being used
            if templates.get(self.factory_name):
                raise GrokError("Multiple possible templates for template %r. It "
                                "uses grok.template('%s'), but there is also "
                                "a template called '%s'."
                                % (factory, template_name, factory_name),
                                factory)

        provides = util.class_annotation(factory, 'grok.provides', IPageTemplate)
        macro = util.class_annotation(factory, 'megrok.template.macro', None)
        contentType = util.class_annotation(factory,
                                    'megrok.template.content_type', 'text/html')
        view_layer = util.class_annotation(factory, 'megrok.layer.layer',
                                       None) or module_info.getAnnotation('megrok.layer.layer',
                                       None) or IBrowserRequest
        view_name = util.class_annotation(factory, 'grok.name', u'')


        filename = template.__grok_location__
        factory = TemplateFactory(filename, contentType, macro)
        templates.markAssociated(template_name)
        zope.interface.directlyProvides(factory, provides)
        zope.component.provideAdapter(factory,
                                 adapts=(view_context, view_layer),
                                 provides=provides,
                                 name=view_name)
        return True



