import os

import zope.component
import zope.interface
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
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
    provides = None

    def grok(self, name, factory, context, module_info, templates):
        view_context = util.determine_class_context(factory, context)
        factory.module_info = module_info
        factory_name = factory.__name__.lower()

        # we need a path to the file containing the template
        template_name = util.class_annotation(factory, 'grok.template',
                                              factory_name)
        filepath = os.path.join(os.path.dirname(module_info.path), template_name)
        if not os.path.exists(filepath):
            filepath = None
            if os.path.exists(template_name):
                filepath = template_name
        if filepath is None:
            raise GrokError("No template found for %s."
                            " Please use grok.template to define path to the"
                            " file containing the template"
                            % (factory.__name__),
                            factory)

        provides = util.class_annotation(factory, 'grok.provides', self.provides)
        macro = util.class_annotation(factory, 'mars.template.macro', None)
        contentType = util.class_annotation(factory,
                                    'mars.template.content_type', 'text/html')
        view_layer = util.class_annotation(factory, 'mars.layer.layer',
                                       None) or module_info.getAnnotation('mars.layer.layer',
                                       None) or IDefaultBrowserLayer
        view_name = util.class_annotation(factory, 'grok.name', '')

        factory = TemplateFactory(filepath, contentType, macro)
        zope.interface.directlyProvides(factory, provides)
        #print '\nname:', view_name,'context:', view_context,'factory:', factory, '\n'
        zope.component.provideAdapter(factory,
                                 adapts=(view_context, view_layer),
                                 provides=provides,
                                 name=view_name)
        return True


class TemplateFactoryGrokker(TemplateFactoryGrokkerBase):
    component_class = mars.template.TemplateFactory
    provides = IPageTemplate

class LayoutFactoryGrokker(TemplateFactoryGrokkerBase):
    component_class = mars.template.LayoutFactory
    provides = ILayoutTemplate


