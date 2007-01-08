import os

import zope.component.interface
from zope import interface, component
from zope.publisher.interfaces.browser import (IDefaultBrowserLayer,
                                               IBrowserRequest,
                                               IBrowserPublisher)
from zope.publisher.interfaces.xmlrpc import IXMLRPCRequest
from zope.security.checker import NamesChecker, defineChecker
from zope.security.permission import Permission
from zope.security.interfaces import IPermission

from zope.app.container.interfaces import IContainer
from zope.app.publisher.xmlrpc import MethodPublisher
from zope.app.container.interfaces import INameChooser

import grok
from grok import util, components, formlib
from grok.error import GrokError


class ModelGrokker(grok.ClassGrokker):
    component_class = grok.Model

    def register(self, context, name, factory, module_info, templates):
        for field in formlib.get_context_schema_fields(factory):
            setattr(factory, field.__name__, field.default)       

class ContainerGrokker(ModelGrokker):
    component_class = grok.Container
    
class LocalUtilityGrokker(ModelGrokker):
    component_class = grok.LocalUtility
    
class AdapterGrokker(grok.ClassGrokker):
    component_class = grok.Adapter

    def register(self, context, name, factory, module_info, templates):
        adapter_context = util.determine_class_context(factory, context)
        provides = util.class_annotation(factory, 'grok.provides', None)
        if provides is None:
            util.check_implements_one(factory)
        name = util.class_annotation(factory, 'grok.name', '')
        component.provideAdapter(factory, adapts=(adapter_context,),
                                 provides=provides,
                                 name=name)
            
class MultiAdapterGrokker(grok.ClassGrokker):
    component_class = grok.MultiAdapter
    
    def register(self, context, name, factory, module_info, templates):
        provides = util.class_annotation(factory, 'grok.provides', None)
        if provides is None:
            util.check_implements_one(factory)
        util.check_adapts(factory)
        name = util.class_annotation(factory, 'grok.name', '')
        component.provideAdapter(factory, provides=provides, name=name)

class GlobalUtilityGrokker(grok.ClassGrokker):
    component_class = grok.GlobalUtility

    def register(self, context, name, factory, module_info, templates):
        provides = util.class_annotation(factory, 'grok.provides', None)
        if provides is None:
            util.check_implements_one(factory)
        name = util.class_annotation(factory, 'grok.name', '')
        component.provideUtility(factory(), provides=provides, name=name)

class XMLRPCGrokker(grok.ClassGrokker):
    component_class = grok.XMLRPC

    def register(self, context, name, factory, module_info, templates):
        view_context = util.determine_class_context(factory, context)
        # XXX We should really not make __FOO__ methods available to
        # the outside -- need to discuss how to restrict such things.
        methods = util.methods_from_class(factory)

        # Determine the default permission for the XMLRPC methods.
        # There can only be 0 or 1 of those.
        permissions = util.class_annotation(factory, 'grok.require', [])
        if not permissions:
            default_permission = None
        elif len(permissions) == 1:
            default_permission = permissions[0]
        else:
            raise GrokError('grok.require was called multiple times in '
                            '%r. It may only be called once on class level.'
                            % factory, factory)

        for method in methods:
            # Make sure that the class inherits MethodPublisher, so that the
            # views have a location
            method_view = type(
                factory.__name__, (factory, MethodPublisher),
                {'__call__': method}
                )
            component.provideAdapter(
                method_view, (view_context, IXMLRPCRequest),
                interface.Interface,
                name=method.__name__)

            # Protect method_view with either the permission that was
            # set on the method, the default permission from the class
            # level or zope.Public.
            permission = getattr(method, '__grok_require__', default_permission)
            if permission is None or permission == 'zope.Public':
                checker = NamesChecker(['__call__'])
            else:
                checker = NamesChecker(['__call__'], permission)
            defineChecker(method_view, checker)

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

        # protect view, public by default
        permissions = util.class_annotation(factory, 'grok.require', [])
        if not permissions:
            checker = NamesChecker(['__call__'])
        elif len(permissions) > 1:
            raise GrokError('grok.require was called multiple times in view '
                            '%r. It may only be called once.' % factory,
                            factory)
        elif permissions[0] == 'zope.Public':
            checker = NamesChecker(['__call__'])
        else:
            perm = permissions[0]
            if component.queryUtility(IPermission, name=perm) is None:
                raise GrokError('Undefined permission %r in view %r. Use '
                                'grok.define_permission first.'
                                % (perm, factory), factory)
            checker = NamesChecker(['__call__'], permissions[0])

        defineChecker(factory, checker)

        # safety belt: make sure that the programmer didn't use
        # @grok.require on any of the view's methods.
        methods = util.methods_from_class(factory)
        for method in methods:
            if getattr(method, '__grok_require__', None) is not None:
                raise GrokError('The @grok.require decorator is used for '
                                'method %r in view %r. It may only be used '
                                'for XML-RPC methods.'
                                % (method.__name__, factory), factory)

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

class GlobalUtilityDirectiveGrokker(grok.ModuleGrokker):

    def register(self, context, module_info, templates):
        infos = module_info.getAnnotation('grok.global_utility', [])
    
        for info in infos:
            if info.provides is None:
                util.check_implements_one(info.factory)
            component.provideUtility(info.factory(),
                                     provides=info.provides,
                                     name=info.name)

class SiteGrokker(grok.ClassGrokker):
    component_class = grok.Site
    priority = 500
    continue_scanning = True

    def register(self, context, name, factory, module_info, templates):
        infos = util.class_annotation_list(factory, 'grok.local_utility', None)
        if infos is None:
            return

        for info in infos:
            if info.public and not IContainer.implementedBy(factory):
                raise GrokError(
                    "Cannot set public to True with grok.local_utility as "
                    "the site (%r) is not a container." %
                    factory, factory)
            if info.provides is None:
                if util.check_subclass(info.factory, grok.LocalUtility):
                    baseInterfaces = interface.implementedBy(grok.LocalUtility)
                    utilityInterfaces = interface.implementedBy(info.factory)
                    provides = list(utilityInterfaces - baseInterfaces)

                    if len(provides) == 0 and len(list(utilityInterfaces)) > 0:
                        raise GrokError(
                            "Cannot determine which interface to use "
                            "for utility registration of %r. "
                            "It implements an interface that is a specialization "
                            "of an interface implemented by grok.LocalUtility. "
                            "Specify the interface by either using grok.provides "
                            "on the utility or passing 'provides' to "
                            "grok.local_utility." % info.factory, info.factory)
                else:
                    provides = list(interface.implementedBy(info.factory))

                util.check_implements_one_from_list(provides, info.factory)
                info.provides = provides[0]

        # Make sure that local utilities from subclasses override
        # utilities from base classes if the registration (provided
        # interface, name) is identical.
        overridden_infos = []
        used = set()
        for info in reversed(infos):
            key = (info.provides, info.name)
            if key in used:
                continue
            used.add(key)
            overridden_infos.append(info)
        overridden_infos.reverse()

        # store infos on site class
        factory.__grok_utilities_to_install__ = overridden_infos
        component.provideHandler(localUtilityRegistrationSubscriber,
                                 adapts=(factory, grok.IObjectAddedEvent))

def localUtilityRegistrationSubscriber(site, event):
    """A subscriber that fires to set up local utilities.
    """
    installed = getattr(site, '__grok_utilities_installed__', False)
    if installed:
        return

    for info in util.class_annotation(site.__class__,
                                      'grok.utilities_to_install', []):
        utility = info.factory()
        site_manager = site.getSiteManager()

        # store utility
        if not info.public:
            container = site_manager
        else:
            container = site

        name_in_container = info.name_in_container 
        if name_in_container is None:
            name_in_container = INameChooser(container).chooseName(
                info.factory.__name__, utility)
        container[name_in_container] = utility

        # execute setup callback
        if info.setup is not None:
            info.setup(utility)

        # register utility
        site_manager.registerUtility(utility, provided=info.provides,
                                     name=info.name)

    # we are done. If this subscriber gets fired again, we therefore
    # do not register utilities anymore
    site.__grok_utilities_installed__ = True
        
class DefinePermissionGrokker(grok.ModuleGrokker):

    priority = 1500

    def register(self, context, module_info, templates):
        permissions = module_info.getAnnotation('grok.define_permission', [])
        for permission in permissions:
            # TODO permission title and description
            component.provideUtility(Permission(permission), name=permission)
