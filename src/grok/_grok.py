##############################################################################
#
# Copyright (c) 2006 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Grok
"""
import sys
import os
from pkg_resources import resource_listdir, resource_exists, resource_string
import persistent
from zope.dottedname.resolve import resolve
from zope import component
from zope import interface
from zope.publisher.browser import BrowserPage
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.pagetemplate import pagetemplate
from zope.app.pagetemplate.engine import TrustedAppPT

from grok import util
from grok.error import GrokError
from grok.directive import (ClassDirectiveContext, ModuleDirectiveContext, ClassOrModuleDirectiveContext,
                            TextDirective, InterfaceOrClassDirective)
     

class Model(persistent.Persistent):
    pass

class Adapter(object):

    def __init__(self, context):
        self.context = context

class MultiAdapter(object):
    pass

class View(BrowserPage):

    def __call__(self):
        self.before()

        template = getattr(self, 'template', None)
        if not template:
            return self.render()

        namespace = template.pt_getContext()
        namespace['request'] = self.request
        namespace['view'] = self
        namespace['context'] = self.context
        return template.pt_render(namespace)

    def before(self):
        pass

class PageTemplate(TrustedAppPT, pagetemplate.PageTemplate):
    expand = 0

    def __init__(self, template):
        super(PageTemplate, self).__init__()
        if util.not_unicode_or_ascii(template):
            raise GrokError("Invalid page template. Page templates must be "
                            "unicode or ASCII.")
        self.write(template)

        # XXX unfortunately using caller_module means that
        # PageTemplate cannot be subclassed
        self.__grok_module__ = caller_module()

AMBIGUOUS_CONTEXT = object()
def grok(dotted_name):
    # TODO for now we only grok modules
    module = resolve(dotted_name)

    context = None
    adapters = []
    multiadapters = []
    views = []
    templates = TemplateRegistry()
    for name in dir(module):
        obj = getattr(module, name)

        if not defined_locally(obj, dotted_name):
            continue

        if util.check_subclass(obj, Model):
            if context is None:
                context = obj
            else:
                context = AMBIGUOUS_CONTEXT
        elif util.check_subclass(obj, Adapter):
            adapters.append(obj)
        elif util.check_subclass(obj, MultiAdapter):
            multiadapters.append(obj)
        elif util.check_subclass(obj, View):
            views.append(obj)
        elif isinstance(obj, PageTemplate):
            templates.register(name, obj)

    # find filesystem resources
    module_name = dotted_name.split('.')[-1]
    directory_name = directive_annotation(module, 'grok.resource', module_name)
    if resource_exists(dotted_name, directory_name):
        resources = resource_listdir(dotted_name, directory_name)
        for resource in resources:
            if not resource.endswith(".pt"):
                continue

            contents = resource_string(dotted_name, os.path.join(directory_name, resource))
            template = PageTemplate(contents)
            template_name = resource[:-3]
            if templates.get(template_name):
                raise GrokError("Conflicting templates found for name '%s' in module %r, "
                                "both inline and in resource directory '%s'."
                                % (template_name, module, directory_name))
            templates.register(template_name, template)

    module_context = directive_annotation(module, 'grok.context', None)
    if module_context:
        context = module_context

    for factory in adapters:
        adapter_context = determine_context(factory, context)
        name = directive_annotation(factory, 'grok.name', '')
        component.provideAdapter(factory, adapts=(adapter_context,), name=name)

    for factory in multiadapters:
        name = directive_annotation(factory, 'grok.name', '')
        component.provideAdapter(factory, name=name)

    for factory in views:
        view_context = determine_context(factory, context)
        factory_name = factory.__name__.lower()

        # find inline templates
        template_name = directive_annotation(factory, 'grok.template', factory_name)
        template = templates.get(template_name)

        if factory_name != template_name:
            # grok.template is being used
            if templates.get(factory_name):
                raise GrokError("Multiple possible templates for view %r. It "
                                "uses grok.template('%s'), but there is also "
                                "a template called '%s'."
                                % (factory, template_name, factory_name))

        if template:
            if getattr(factory, 'render', None):
                raise GrokError("Multiple possible ways to render view %r. "
                                "It has both a 'render' method as well as "
                                "an associated template." % factory)

            templates.markAssociated(template_name)
            factory.template = template
        else:
            if not getattr(factory, 'render', None):
                raise GrokError("View %r has no associated template or "
                                "'render' method." % factory)

        view_name = directive_annotation(factory, 'grok.name', factory_name)
        component.provideAdapter(factory,
                                 adapts=(view_context, IDefaultBrowserLayer),
                                 provides=interface.Interface,
                                 name=view_name)

    for name, unassociated in templates.listUnassociatedTemplates():
        source = '<%s template in %s>' % (name, dotted_name)
        check_context(source, context)

        class TemplateView(View):
            template = unassociated

        templates.markAssociated(name)

        component.provideAdapter(TemplateView,
                                 adapts=(context, IDefaultBrowserLayer),
                                 provides=interface.Interface,
                                 name=name)

class TemplateRegistry(object):

    def __init__(self):
        self._reg = {}

    def register(self, name, template):
        self._reg[name] = dict(template=template, associated=False)

    def markAssociated(self, name):
        self._reg[name]['associated'] = True

    def get(self, name):
        entry = self._reg.get(name)
        if entry is None:
            return None
        return entry['template']

    def listUnassociatedTemplates(self):
        for name, entry in self._reg.iteritems():
            if not entry['associated']:
                yield name, entry['template']

def defined_locally(obj, dotted_name):
    obj_module = getattr(obj, '__grok_module__', None)
    if obj_module is None:
        obj_module = getattr(obj, '__module__', None)
    return obj_module == dotted_name

def check_context(source, context):
    if context is None:
        raise GrokError("No module-level context for %s, please use "
                        "grok.context." % source)
    elif context is AMBIGUOUS_CONTEXT:
        raise GrokError("Multiple possible contexts for %s, please use "
                        "grok.context." % source)

def determine_context(factory, module_context):
    context = directive_annotation(factory, 'grok.context', module_context)
    check_context(repr(factory), context)
    return context

def directive_annotation(obj, name, default):
    return getattr(obj, '__%s__' % name.replace('.', '_'), default)

def caller_module():
    return sys._getframe(2).f_globals['__name__']

# directives
name = TextDirective('grok.name', ClassDirectiveContext())
template = TextDirective('grok.template', ClassDirectiveContext())
context = InterfaceOrClassDirective('grok.context', ClassOrModuleDirectiveContext())
resource = TextDirective('grok.resource', ModuleDirectiveContext())
