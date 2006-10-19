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
import inspect

from zope import component
from zope import interface
import zope.component.interface
from zope.component.interfaces import IDefaultViewName
from zope.security.checker import (defineChecker, getCheckerForInstancesOf,
                                   NoProxy)
from zope.publisher.interfaces.browser import (IDefaultBrowserLayer,
                                               IBrowserRequest,
                                               IBrowserPublisher)

from zope.app.publisher.xmlrpc import MethodPublisher
from zope.publisher.interfaces.xmlrpc import IXMLRPCRequest

import grok

from grok import util, scan, components, security
from grok.error import GrokError, GrokImportError
from grok.directive import (ClassDirectiveContext, ModuleDirectiveContext,
                            ClassOrModuleDirectiveContext,
                            TextDirective, InterfaceOrClassDirective,
                            frame_is_module, frame_is_class)


_bootstrapped = False
def bootstrap():
    component.provideAdapter(components.ModelTraverser)
    # register the name 'index' as the default view name
    component.provideAdapter('index',
                             adapts=(grok.Model, IBrowserRequest),
                             provides=IDefaultViewName)

# add a cleanup hook so that grok will bootstrap itself again whenever
# the Component Architecture is torn down.
def resetBootstrap():
    global _bootstrapped
    _bootstrapped = False
from zope.testing.cleanup import addCleanUp
addCleanUp(resetBootstrap)


def do_grok(dotted_name):
    global _bootstrapped
    if not _bootstrapped:
        bootstrap()
        _bootstrapped = True

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
    (models, adapters, multiadapters, utilities, views, xmlrpc_views,
     traversers, templates, subscribers) = scan_module(module_info)

    find_filesystem_templates(module_info, templates)

    context = util.determine_module_context(module_info, models)

    register_models(models)
    register_adapters(context, adapters)
    register_multiadapters(multiadapters)
    register_utilities(utilities)
    register_views(context, views, templates)
    register_xmlrpc(context, xmlrpc_views)
    register_traversers(context, traversers)
    register_unassociated_templates(context, templates, module_info)
    register_subscribers(subscribers)


def scan_module(module_info):
    components = {
            grok.Model: [],
            grok.Adapter: [],
            grok.MultiAdapter: [],
            grok.Utility: [],
            grok.View: [],
            grok.XMLRPC: [],
            grok.Traverser: []
            }
    templates = TemplateRegistry()
    subscribers = module_info.getAnnotation('grok.subscribers', [])

    module = module_info.getModule()
    for name in dir(module):
        obj = getattr(module, name)

        if not util.defined_locally(obj, module_info.dotted_name):
            continue

        if isinstance(obj, grok.PageTemplate):
            templates.register(name, obj)
            obj._annotateGrokInfo(name, module_info.dotted_name)
            continue
        # XXX refactor
        elif util.check_subclass(obj, grok.View):
            obj.module_info = module_info
            components[grok.View].append(obj)
            continue

        for candidate_class, found_list in components.items():
            if util.check_subclass(obj, candidate_class):
                found_list.append(obj)
                break

    return (components[grok.Model], components[grok.Adapter], 
            components[grok.MultiAdapter], components[grok.Utility],
            components[grok.View], components[grok.XMLRPC],
            components[grok.Traverser], templates, subscribers)

def find_filesystem_templates(module_info, templates):
    template_dir_name = module_info.getAnnotation('grok.templatedir',
                                                  module_info.name)
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

            template = grok.PageTemplate(contents)
            template._annotateGrokInfo(template_name, template_path)

            inline_template = templates.get(template_name)
            if inline_template:
                raise GrokError("Conflicting templates found for name '%s' "
                                "in module %r, both inline and in template "
                                "directory '%s'."
                                % (template_name, module_info.getModule(),
                                   template_dir), inline_template)
            templates.register(template_name, template)


def register_static_resources(dotted_name, resource_directory):
    resource_factory = components.DirectoryResourceFactory(resource_directory,
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
        adapter_context = util.determine_class_context(factory, context)
        util.check_implements_one(factory)
        name = util.class_annotation(factory, 'grok.name', '')
        component.provideAdapter(factory, adapts=(adapter_context,), name=name)

def register_multiadapters(multiadapters):
    for factory in multiadapters:
        util.check_implements_one(factory)
        util.check_adapts(factory)
        name = util.class_annotation(factory, 'grok.name', '')
        component.provideAdapter(factory, name=name)

def register_utilities(utilities):
    for factory in utilities:
        util.check_implements_one(factory)
        name = util.class_annotation(factory, 'grok.name', '')
        component.provideUtility(factory(), name=name)

def register_xmlrpc(context, views):
    for view in views:
        view_context = util.determine_class_context(view, context)
        candidates = [getattr(view, name) for name in dir(view)]
        methods = [c for c in candidates if inspect.ismethod(c)]

        for method in methods:
            # Make sure that the class inherits MethodPublisher, so that the views
            # have a location
            method_view = type(view.__name__, (view, MethodPublisher), 
                               {'__call__': method,
                                '__Security_checker__': security.GrokChecker()}
                               )
            component.provideAdapter(
                method_view, (view_context, IXMLRPCRequest), interface.Interface,
                name=method.__name__)

def register_views(context, views, templates):
    for factory in views:
        view_context = util.determine_class_context(factory, context)
        factory_name = factory.__name__.lower()

        # find inline templates
        template_name = util.class_annotation(factory, 'grok.template',
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

        view_name = util.class_annotation(factory, 'grok.name', factory_name)
        component.provideAdapter(factory,
                                 adapts=(view_context, IDefaultBrowserLayer),
                                 provides=interface.Interface,
                                 name=view_name)

        # TODO minimal security here (read: everything is public)
        defineChecker(factory, NoProxy)

def register_traversers(context, traversers):
    for factory in traversers:
        factory_context = util.determine_class_context(factory, context)
        component.provideAdapter(factory,
                                 adapts=(factory_context, IBrowserRequest),
                                 provides=IBrowserPublisher)

def register_unassociated_templates(context, templates, module_info):
    for name, unassociated in templates.listUnassociatedTemplates():
        util.check_context(unassociated, context)

        module_info_ = module_info
        class TemplateView(grok.View):
            template = unassociated
            module_info = module_info_

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

def traverseDecorator(function):
    frame = sys._getframe(1)
    if not frame_is_class(frame):
        raise GrokImportError("@grok.traverse can only be used on class "
                              "level.")

    if '__grok_traverse__' in frame.f_locals:
        raise GrokImportError("@grok.traverse can only be used once per class.")

    frame.f_locals['__grok_traverse__'] = function
