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
import zope.component.interface
from zope.component.interfaces import IDefaultViewName
from zope.security.checker import defineChecker, getCheckerForInstancesOf, NoProxy
from zope.publisher.browser import BrowserPage
from zope.publisher.interfaces.browser import IDefaultBrowserLayer, IBrowserRequest
from zope.pagetemplate import pagetemplate
from zope.app.pagetemplate.engine import TrustedAppPT
from zope.app.publisher.browser.directoryresource import DirectoryResourceFactory

from grok import util, scan
from grok.error import GrokError, GrokImportError
from grok.directive import (ClassDirectiveContext, ModuleDirectiveContext,
                            ClassOrModuleDirectiveContext,
                            TextDirective, InterfaceOrClassDirective, frame_is_module)

AMBIGUOUS_CONTEXT = object()

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
            raise ValueError("Invalid page template. Page templates must be "
                             "unicode or ASCII.")
        self.write(template)

        # XXX unfortunately using caller_module means that
        # PageTemplate cannot be subclassed
        self.__grok_module__ = caller_module()

    def __repr__(self):
        return '<%s template in %s>' % (self.__grok_name__, self.__grok_location__)

def grok(dotted_name):
    # register the name 'index' as the default view name
    # TODO this needs to be moved to grok startup time (similar to ZCML-time)
    component.provideAdapter('index',
                             adapts=(Model, IBrowserRequest),
                             provides=IDefaultViewName)

    package_or_module = resolve(dotted_name)
    for name, path in scan.modules(dotted_name, package_or_module.__file__):
        if is_package(name):
            register_static_resources(name, path)

        grok_module(name)

def grok_module(dotted_name):
    module = resolve(dotted_name)

    models, adapters, multiadapters, views, templates, subscribers = scan_module(dotted_name, module)
    
    find_filesystem_templates(dotted_name, module, templates)

    context = determine_module_context(module, models)

    register_models(models)
    register_adapters(context, adapters)
    register_multiadapters(multiadapters)
    register_views(context, views, templates)
    register_unassociated_templates(context, templates)
    register_subscribers(subscribers)

def scan_module(dotted_name, module):
    models = []
    adapters = []
    multiadapters = []
    views = []
    templates = TemplateRegistry()
    subscribers = getattr(module, '__grok_subscribers__', [])

    for name in dir(module):
        obj = getattr(module, name)

        if not defined_locally(obj, dotted_name):
            continue

        if util.check_subclass(obj, Model):
            models.append(obj)
        elif util.check_subclass(obj, Adapter):
            adapters.append(obj)
        elif util.check_subclass(obj, MultiAdapter):
            multiadapters.append(obj)
        elif util.check_subclass(obj, View):
            views.append(obj)
        elif isinstance(obj, PageTemplate):
            templates.register(name, obj)
            obj.__grok_name__ = name
            obj.__grok_location__ = dotted_name

    return models, adapters, multiadapters, views, templates, subscribers

def find_filesystem_templates(dotted_name, module, templates):
    module_name = dotted_name.split('.')[-1]
    directory_name = directive_annotation(module, 'grok.templatedir', module_name)
    if resource_exists(dotted_name, directory_name):
        template_files = resource_listdir(dotted_name, directory_name)
        for template_file in template_files:
            if template_file.startswith('.') or template_file.endswith('~'):
                continue

            template_name = template_file[:-3]
            template_path = os.path.join(directory_name, template_file)

            if not template_file.endswith('.pt'):
                raise GrokError("Unrecognized file '%s' in template directory '%s'."
                                % (template_file, directory_name), module)

            contents = resource_string(dotted_name, template_path)
            template = PageTemplate(contents)
            template.__grok_name__ = template_name
            # XXX is this zip-safe?
            template.__grok_location__ = os.path.join(
                os.path.dirname(module.__file__), template_path)

            inline_template = templates.get(template_name)
            if inline_template:
                raise GrokError("Conflicting templates found for name '%s' "
                                "in module %r, both inline and in template "
                                "directory '%s'."
                                % (template_name, module, directory_name),
                                inline_template)
            templates.register(template_name, template)

def register_static_resources(dotted_name, package_directory):
    path = os.path.join(package_directory, 'static')

    if os.path.exists(path):
#         if not os.path.isdir(path):
#             raise GrokError("")

        resource_factory = DirectoryResourceFactory(path, NoProxy, dotted_name)
        component.provideAdapter(resource_factory, (IDefaultBrowserLayer,),
                                 interface.Interface, name=dotted_name)

def register_models(models):
    for model in models:
        # TODO minimal security here (read: everything is public)
        if not getCheckerForInstancesOf(model):
            defineChecker(model, NoProxy)

def register_adapters(context, adapters):
    for factory in adapters:
        adapter_context = determine_class_context(factory, context)
        name = directive_annotation(factory, 'grok.name', '')
        component.provideAdapter(factory, adapts=(adapter_context,), name=name)

def register_multiadapters(multiadapters):
    for factory in multiadapters:
        name = directive_annotation(factory, 'grok.name', '')
        component.provideAdapter(factory, name=name)

def register_views(context, views, templates):
    for factory in views:
        view_context = determine_class_context(factory, context)
        factory_name = factory.__name__.lower()

        # find inline templates
        template_name = directive_annotation(factory, 'grok.template',
                                             factory_name)
        template = templates.get(template_name)

        if factory_name != template_name:
            # grok.template is being used
            if templates.get(factory_name):
                raise GrokError("Multiple possible templates for view %r. It "
                                "uses grok.template('%s'), but there is also "
                                "a template called '%s'."
                                % (factory, template_name, factory_name),
                                factory)

        if template:
            if getattr(factory, 'render', None):
                raise GrokError("Multiple possible ways to render view %r. "
                                "It has both a 'render' method as well as "
                                "an associated template." % factory,
                                factory)

            templates.markAssociated(template_name)
            factory.template = template
        else:
            if not getattr(factory, 'render', None):
                raise GrokError("View %r has no associated template or "
                                "'render' method." % factory,
                                factory)

        view_name = directive_annotation(factory, 'grok.name', factory_name)
        component.provideAdapter(factory,
                                 adapts=(view_context, IDefaultBrowserLayer),
                                 provides=interface.Interface,
                                 name=view_name)

        # TODO minimal security here (read: everything is public)
        defineChecker(factory, NoProxy)

def register_unassociated_templates(context, templates):
    for name, unassociated in templates.listUnassociatedTemplates():
        check_context(unassociated, context)

        class TemplateView(View):
            template = unassociated

        templates.markAssociated(name)

        component.provideAdapter(TemplateView,
                                 adapts=(context, IDefaultBrowserLayer),
                                 provides=interface.Interface,
                                 name=name)

        # TODO minimal security here (read: everything is public)
        defineChecker(TemplateView, NoProxy)

def register_subscribers(subscribers):
    for factory, subscribed in subscribers:
        component.provideHandler(factory, adapts=subscribed)
        for iface in subscribed:
            zope.component.interface.provideInterface('', iface)

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

def check_context(component, context):
    if context is None:
        raise GrokError("No module-level context for %r, please use "
                        "grok.context." % component, component)
    elif context is AMBIGUOUS_CONTEXT:
        raise GrokError("Multiple possible contexts for %r, please use "
                        "grok.context." % component, component)

def determine_module_context(module, models):
    if len(models) == 0:
        context = None
    elif len(models) == 1:
        context = models[0]
    else:
        context = AMBIGUOUS_CONTEXT

    module_context = directive_annotation(module, 'grok.context', None)
    if module_context:
        context = module_context

    return context
    
def determine_class_context(class_, module_context):
    context = directive_annotation(class_, 'grok.context', module_context)
    check_context(class_, context)
    return context

def directive_annotation(obj, name, default):
    return getattr(obj, '__%s__' % name.replace('.', '_'), default)

def caller_module():
    return sys._getframe(2).f_globals['__name__']

# directives
name = TextDirective('grok.name', ClassDirectiveContext())
template = TextDirective('grok.template', ClassDirectiveContext())
context = InterfaceOrClassDirective('grok.context',
                                    ClassOrModuleDirectiveContext())
templatedir = TextDirective('grok.templatedir', ModuleDirectiveContext())

# decorators
class SubscribeDecorator:
    def __init__(self, *args):
        self.subscribed = args

    def __call__(self, function):
        frame = sys._getframe(1)
        if not frame_is_module(frame):
            raise GrokImportError("@grok.subscribe can only be used on module level.")

        if not self.subscribed:
            raise GrokImportError("@grok.subscribe requires at least one argument.")

        subscribers = frame.f_locals.get('__grok_subscribers__', None)
        if subscribers is None:
            frame.f_locals['__grok_subscribers__'] = subscribers = []
        subscribers.append((function, self.subscribed))
