import os
import inspect

import zope.component.interface
from zope import interface, component
from zope.security.checker import (defineChecker, getCheckerForInstancesOf,
                                   NoProxy)
from zope.publisher.interfaces.browser import (IDefaultBrowserLayer,
                                               IBrowserRequest,
                                               IBrowserPublisher)
from zope.app.publisher.xmlrpc import MethodPublisher
from zope.publisher.interfaces.xmlrpc import IXMLRPCRequest

import grok
from grok import util, components, security, formlib
from grok.error import GrokError

class ModelGrokker(grok.ClassGrokker):
    component_class = grok.Model

    def register(self, context, name, factory, module_info, templates):
        if not getCheckerForInstancesOf(factory):
            defineChecker(factory, NoProxy)

        for field in formlib.get_context_schema_fields(factory):
            setattr(factory, field.__name__, field.default)       

class ContainerGrokker(ModelGrokker):
    component_class = grok.Container
    
class AdapterGrokker(grok.ClassGrokker):
    component_class = grok.Adapter

    def register(self, context, name, factory, module_info, templates):
        adapter_context = util.determine_class_context(factory, context)
        util.check_implements_one(factory)
        name = util.class_annotation(factory, 'grok.name', '')
        try:
            component.provideAdapter(factory, adapts=(adapter_context,),
                                     name=name)
        except TypeError:
            import pdb; pdb.set_trace()
            
class MultiAdapterGrokker(grok.ClassGrokker):
    component_class = grok.MultiAdapter
    
    def register(self, context, name, factory, module_info, templates):
        util.check_implements_one(factory)
        util.check_adapts(factory)
        name = util.class_annotation(factory, 'grok.name', '')
        component.provideAdapter(factory, name=name)

class UtilityGrokker(grok.ClassGrokker):
    component_class = grok.Utility

    def register(self, context, name, factory, module_info, templates):
        util.check_implements_one(factory)
        name = util.class_annotation(factory, 'grok.name', '')
        component.provideUtility(factory(), name=name)

class XMLRPCGrokker(grok.ClassGrokker):
    component_class = grok.XMLRPC
    
    def register(self, context, name, factory, module_info, templates):
        view_context = util.determine_class_context(factory, context)
        candidates = [getattr(factory, name) for name in dir(factory)]
        methods = [c for c in candidates if inspect.ismethod(c)]

        for method in methods:
            # Make sure that the class inherits MethodPublisher, so that the
            # views have a location
            method_view = type(
                factory.__name__, (factory, MethodPublisher),
                {'__call__': method,
                 '__Security_checker__': security.GrokChecker()}
                )
            component.provideAdapter(
                method_view, (view_context, IXMLRPCRequest),
                interface.Interface,
                name=method.__name__)

class ViewGrokker(grok.ClassGrokker):
    component_class = grok.View

    def register(self, context, name, factory, module_info, templates):
        view_context = util.determine_class_context(factory, context)

        factory.module_info = module_info

        # some extra work to take care of if this view is a form
        if util.check_subclass(factory, components.EditForm):
            formlib.setup_editform(factory, view_context)
        elif util.check_subclass(factory, components.DisplayForm):
            formlib.setup_displayform(factory, view_context)
        elif util.check_subclass(factory, components.AddForm):
            formlib.setup_addform(factory, view_context)

        factory_name = factory.__name__.lower()

        # find templates
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

        # we never accept a 'render' method for forms
        if util.check_subclass(factory, components.Form):
            if getattr(factory, 'render', None):
                raise GrokError(
                    "It is not allowed to specify a custom 'render' "
                    "method for form %r. Forms either use the default "
                    "template or a custom-supplied one." % factory,
                    factory)

        if template:
            if getattr(factory, 'render', None):
                # we do not accept render and template both for a view
                raise GrokError(
                    "Multiple possible ways to render view %r. "
                    "It has both a 'render' method as well as "
                    "an associated template." % factory,
                    factory)

            templates.markAssociated(template_name)
            factory.template = template
        else:
            if not getattr(factory, 'render', None):
                if util.check_subclass(factory, components.EditForm):
                    # we have a edit form without template
                    factory.template = formlib.defaultEditTemplate
                elif util.check_subclass(factory, components.DisplayForm):
                    # we have a display form without template
                    factory.template = formlib.defaultDisplayTemplate
                elif util.check_subclass(factory, components.AddForm):
                    # we have an add form without template
                    factory.template = formlib.defaultEditTemplate
                else:
                    # we do not accept a view without any way to render it
                    raise GrokError("View %r has no associated template or "
                                    "'render' method." % factory,
                                    factory)

        view_name = util.class_annotation(factory, 'grok.name',
                                          factory_name)
        # __view_name__ is needed to support IAbsoluteURL on views
        factory.__view_name__ = view_name
        component.provideAdapter(factory,
                                 adapts=(view_context, IDefaultBrowserLayer),
                                 provides=interface.Interface,
                                 name=view_name)

        # TODO minimal security here (read: everything is public)
        defineChecker(factory, NoProxy)

class TraverserGrokker(grok.ClassGrokker):
    component_class = grok.Traverser

    def register(self, context, name, factory, module_info, templates):
        factory_context = util.determine_class_context(factory, context)
        component.provideAdapter(factory,
                                 adapts=(factory_context, IBrowserRequest),
                                 provides=IBrowserPublisher)
    
class ModulePageTemplateGrokker(grok.InstanceGrokker):
    # this needs to happen before any other grokkers execute that actually
    # use the templates
    priority = 1000

    component_class = grok.PageTemplate

    def register(self, context, name, instance, module_info, templates):
        templates.register(name, instance)
        instance._annotateGrokInfo(name, module_info.dotted_name)

class FilesystemPageTemplateGrokker(grok.ModuleGrokker):
    # do this early on, but after ModulePageTemplateGrokker, as
    # findFilesystem depends on module-level templates to be
    # already grokked for error reporting
    priority = 999
    
    def register(self, context, module_info, templates):
        templates.findFilesystem(module_info)

class SubscriberGrokker(grok.ModuleGrokker):

    def register(self, context, module_info, templates):
        subscribers = module_info.getAnnotation('grok.subscribers', [])
    
        for factory, subscribed in subscribers:
            component.provideHandler(factory, adapts=subscribed)
            for iface in subscribed:
                zope.component.interface.provideInterface('', iface)

class StaticResourcesGrokker(grok.ModuleGrokker):

    def register(self, context, module_info, templates):
        # we're only interested in static resources if this module
        # happens to be a package
        if not module_info.isPackage():
            return
        
        resource_path = module_info.getResourcePath('static')
        if os.path.isdir(resource_path):
            static_module = module_info.getSubModuleInfo('static')
            if static_module is not None:
                if static_module.isPackage():
                    raise GrokError(
                        "The 'static' resource directory must not "
                        "be a python package.",
                        module_info.getModule())
                else:
                    raise GrokError(
                        "A package can not contain both a 'static' "
                        "resource directory and a module named "
                        "'static.py'", module_info.getModule())
        
        resource_factory = components.DirectoryResourceFactory(
            resource_path, module_info.dotted_name)
        component.provideAdapter(
            resource_factory, (IDefaultBrowserLayer,),
            interface.Interface, name=module_info.dotted_name)
