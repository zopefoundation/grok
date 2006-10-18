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
import os
import sys

import persistent
from zope import component
from zope import interface
from zope.proxy import removeAllProxies
from zope.dottedname.resolve import resolve
import zope.component.interface
from zope.component.interfaces import IDefaultViewName
from zope.security.checker import (defineChecker, getCheckerForInstancesOf,
                                   NoProxy)
from zope.publisher.browser import BrowserPage
from zope.publisher.interfaces.browser import (IDefaultBrowserLayer,
                                               IBrowserRequest)
from zope.pagetemplate import pagetemplate
from zope.app.pagetemplate.engine import TrustedAppPT
from zope.app.publisher.browser import directoryresource
from zope.app.publisher.browser.pagetemplateresource import \
    PageTemplateResourceFactory

from grok import util, scan
from grok.error import GrokError, GrokImportError
from grok.directive import (ClassDirectiveContext, ModuleDirectiveContext,
                            ClassOrModuleDirectiveContext,
                            TextDirective, InterfaceOrClassDirective,
                            frame_is_module)

AMBIGUOUS_CONTEXT = object()

class Model(persistent.Persistent):
    pass

class Adapter(object):

    def __init__(self, context):
        self.context = context

class MultiAdapter(object):
    pass

class View(BrowserPage):

    def __init__(self, context, request):
        self.context = removeAllProxies(context)
        self.request = removeAllProxies(request)

    def __call__(self):
        self.before()

        template = getattr(self, 'template', None)
        if not template:
            return self.render()

        namespace = template.pt_getContext()
        namespace['request'] = self.request
        # Jim would say: WAAAAAAAAAAAAH!
        namespace['view'] = self
        namespace['context'] = removeAllProxies(self.context)

        module_info = template.__grok_module_info__
        directory_resource = component.queryAdapter(self.request,
                interface.Interface, name=module_info.package_dotted_name)
        # XXX need to check whether we really want None here
        namespace['static'] = directory_resource
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

        # __grok_module__ is needed to make defined_locally() return True for
        # inline templates
        # XXX unfortunately using caller_module means that
        # PageTemplate cannot be subclassed
        self.__grok_module__ = caller_module()

    def __repr__(self):
        return '<%s template in %s>' % (self.__grok_name__,
                                        self.__grok_location__)

    def _annotateGrokInfo(self, module_info, name, location):
        self.__grok_module_info__ = module_info
        self.__grok_name__ = name
        self.__grok_location__ = location


def grok(dotted_name):
    # register the name 'index' as the default view name
    # TODO this needs to be moved to grok startup time (similar to ZCML-time)
    component.provideAdapter('index',
                             adapts=(Model, IBrowserRequest),
                             provides=IDefaultViewName)

    module_info = scan.module_info_from_dotted_name(dotted_name)
    grok_tree(module_info)


def grok_tree(module_info):
    grok_module(module_info)

    if not module_info.isPackage():
        return

    resource_path = module_info.getResourcePath('static')
    if os.path.isdir(resource_path):
        static_module = module_info.getSubModuleInfo('static')
        if static_module is not None:
            if static_module.isPackage():
                raise GrokError("The 'static' resource directory must not "
                                "be a python package.", module_info.getModule())
            else:
                raise GrokError("A package can not contain both a 'static' "
                                "resource directory and a module named "
                                "'static.py'", module_info.getModule())
                
        register_static_resources(module_info.dotted_name, resource_path)

    for sub_module_info in module_info.getSubModuleInfos():
        grok_tree(sub_module_info)


def grok_module(module_info):
    (models, adapters, multiadapters,
     views, templates, subscribers) = scan_module(module_info)

    find_filesystem_templates(module_info, templates)

    context = determine_module_context(module_info, models)

    register_models(models)
    register_adapters(context, adapters)
    register_multiadapters(multiadapters)
    register_views(context, views, templates)
    register_unassociated_templates(context, templates)
    register_subscribers(subscribers)

def scan_module(module_info):
    models = []
    adapters = []
    multiadapters = []
    views = []
    templates = TemplateRegistry()
    subscribers = module_info.getAnnotation('grok.subscribers', [])

    module = module_info.getModule()
    for name in dir(module):
        obj = getattr(module, name)

        if not defined_locally(obj, module_info.dotted_name):
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
            obj._annotateGrokInfo(module_info, name, module_info.dotted_name)

    return models, adapters, multiadapters, views, templates, subscribers

def find_filesystem_templates(module_info, templates):
    template_dir_name = module_info.getAnnotation('grok.templatedir', module_info.name)
    template_dir = module_info.getResourcePath(template_dir_name)
    if os.path.isdir(template_dir):
        template_files = os.listdir(template_dir)
        for template_file in template_files:
            if template_file.startswith('.') or template_file.endswith('~'):
                continue

            if not template_file.endswith('.pt'):
                raise GrokError("Unrecognized file '%s' in template directory "
                                "'%s'." % (template_file, template_dir),
                                module_info.getModule())

            template_name = template_file[:-3] # cut off .pt
            template_path = os.path.join(template_dir, template_file)

            f = open(template_path, 'rb')
            contents = f.read()
            f.close()

            template = PageTemplate(contents)
            template._annotateGrokInfo(module_info, template_name,
                                       template_path)
            #template.__grok_name__ = template_name
            #template.__grok_location__ = template_path

            inline_template = templates.get(template_name)
            if inline_template:
                raise GrokError("Conflicting templates found for name '%s' "
                                "in module %r, both inline and in template "
                                "directory '%s'."
                                % (template_name, module_info.getModule(),
                                   template_dir), inline_template)
            templates.register(template_name, template)


class GrokDirectoryResource(directoryresource.DirectoryResource):
    # We subclass this, because we want to override the default factories for
    # the resources so that .pt and .html do not get created as page
    # templates

    resource_factories = {}
    for type, factory in (directoryresource.DirectoryResource.
                          resource_factories.items()):
        if factory is PageTemplateResourceFactory:
            continue
        resource_factories[type] = factory


class GrokDirectoryResourceFactory(object):
    # We need this to allow hooking up our own GrokDirectoryResource
    # and to set the checker to None (until we have our own checker)

    def __init__(self, path, name):
        # XXX we're not sure about the checker=None here
        self.__dir = directoryresource.Directory(path, None, name)
        self.__name = name

    def __call__(self, request):
        resource = GrokDirectoryResource(self.__dir, request)
        resource.__Security_checker__ = GrokChecker()
        resource.__name__ = self.__name
        return resource

class GrokChecker(object):
    # ME GROK ANGRY.
    # ME GROK NOT KNOW WHY CHECKER.

    # We have no idea why we need a custom checker here. One hint was
    # that the DirectoryResource already does something manually with
    # setting up the 'correct' checker for itself and we seem to interfere
    # with that. However, we couldn't figure out what's going on and this
    # solves our problem for now. 

    # XXX re-implement this in a sane way.

    def __init__(self):
        pass

    def check_getattr(self, object, name):
        pass

    def check_setattr(self, ob, name):
        pass

    def check(self, ob, operation):
        pass

    def proxy(self, value):
        return value


def register_static_resources(dotted_name, resource_directory):
    resource_factory = GrokDirectoryResourceFactory(resource_directory,
                                                    dotted_name)
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
        name = class_annotation(factory, 'grok.name', '')
        component.provideAdapter(factory, adapts=(adapter_context,), name=name)

def register_multiadapters(multiadapters):
    for factory in multiadapters:
        name = class_annotation(factory, 'grok.name', '')
        component.provideAdapter(factory, name=name)

def register_views(context, views, templates):
    for factory in views:
        view_context = determine_class_context(factory, context)
        factory_name = factory.__name__.lower()

        # find inline templates
        template_name = class_annotation(factory, 'grok.template',
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

        view_name = class_annotation(factory, 'grok.name', factory_name)
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

def determine_module_context(module_info, models):
    if len(models) == 0:
        context = None
    elif len(models) == 1:
        context = models[0]
    else:
        context = AMBIGUOUS_CONTEXT

    module_context = module_info.getAnnotation('grok.context', None)
    if module_context:
        context = module_context

    return context

def determine_class_context(class_, module_context):
    context = class_annotation(class_, 'grok.context', module_context)
    check_context(class_, context)
    return context

def class_annotation(obj, name, default):
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
            raise GrokImportError("@grok.subscribe can only be used on module "
                                  "level.")

        if not self.subscribed:
            raise GrokImportError("@grok.subscribe requires at least one "
                                  "argument.")

        subscribers = frame.f_locals.get('__grok_subscribers__', None)
        if subscribers is None:
            frame.f_locals['__grok_subscribers__'] = subscribers = []
        subscribers.append((function, self.subscribed))
