##############################################################################
#
# Copyright (c) 2006-2007 Zope Corporation and Contributors.
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
"""Grokkers for the various components."""

import os

import zope.component.interface
from zope import interface, component
from zope.publisher.interfaces.browser import (IDefaultBrowserLayer,
                                               IBrowserRequest,
                                               IBrowserPublisher,
                                               IBrowserSkinType)
from zope.publisher.interfaces.xmlrpc import IXMLRPCRequest
from zope.security.permission import Permission
from zope.app.securitypolicy.role import Role
from zope.app.securitypolicy.rolepermission import rolePermissionManager

from zope.annotation.interfaces import IAnnotations

from zope.app.publisher.xmlrpc import MethodPublisher
from zope.app.container.interfaces import IContainer
from zope.app.container.interfaces import INameChooser
from zope.app.container.contained import contained

from zope.app.intid import IntIds
from zope.app.intid.interfaces import IIntIds
from zope.app.catalog.catalog import Catalog
from zope.app.catalog.interfaces import ICatalog

from zope.exceptions.interfaces import DuplicationError

import martian
from martian.error import GrokError
from martian import util

import grok
from grok import components, formlib
from grok.util import (check_adapts, get_default_permission, make_checker,
                       register_translations_directory)


class AdapterGrokker(martian.ClassGrokker):
    component_class = grok.Adapter

    def grok(self, name, factory, context, module_info, templates):
        adapter_context = util.determine_class_context(factory, context)
        provides = util.class_annotation(factory, 'grok.provides', None)
        if provides is None:
            util.check_implements_one(factory)
        name = util.class_annotation(factory, 'grok.name', '')
        component.provideAdapter(factory, adapts=(adapter_context,),
                                 provides=provides,
                                 name=name)
        return True


class MultiAdapterGrokker(martian.ClassGrokker):
    component_class = grok.MultiAdapter

    def grok(self, name, factory, context, module_info, templates):
        provides = util.class_annotation(factory, 'grok.provides', None)
        if provides is None:
            util.check_implements_one(factory)
        check_adapts(factory)
        name = util.class_annotation(factory, 'grok.name', '')
        component.provideAdapter(factory, provides=provides, name=name)
        return True


class GlobalUtilityGrokker(martian.ClassGrokker):
    component_class = grok.GlobalUtility

    def grok(self, name, factory, context, module_info, templates):
        provides = util.class_annotation(factory, 'grok.provides', None)
        if provides is None:
            util.check_implements_one(factory)
        name = util.class_annotation(factory, 'grok.name', '')
        component.provideUtility(factory(), provides=provides, name=name)
        return True


class XMLRPCGrokker(martian.ClassGrokker):
    component_class = grok.XMLRPC

    def grok(self, name, factory, context, module_info, templates):
        view_context = util.determine_class_context(factory, context)
        # XXX We should really not make __FOO__ methods available to
        # the outside -- need to discuss how to restrict such things.
        methods = util.methods_from_class(factory)

        default_permission = get_default_permission(factory)

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
            permission = getattr(method, '__grok_require__',
                                 default_permission)
            make_checker(factory, method_view, permission)
        return True


class ViewGrokker(martian.ClassGrokker):
    component_class = grok.View

    def grok(self, name, factory, context, module_info, templates):

        view_context = util.determine_class_context(factory, context)

        factory.module_info = module_info
        factory_name = factory.__name__.lower()

        if util.check_subclass(factory, components.GrokForm):
            # setup form_fields from context class if we've encountered a form
            if getattr(factory, 'form_fields', None) is None:
                factory.form_fields = formlib.get_auto_fields(view_context)

            if not getattr(factory.render, 'base_method', False):
                raise GrokError(
                    "It is not allowed to specify a custom 'render' "
                    "method for form %r. Forms either use the default "
                    "template or a custom-supplied one." % factory,
                    factory)

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

        if template:
            if (getattr(factory, 'render', None) and not
                util.check_subclass(factory, components.GrokForm)):
                # we do not accept render and template both for a view
                # (unless it's a form, they happen to have render.
                raise GrokError(
                    "Multiple possible ways to render view %r. "
                    "It has both a 'render' method as well as "
                    "an associated template." % factory, factory)

            templates.markAssociated(template_name)
            factory.template = template
        else:
            if not getattr(factory, 'render', None):
                # we do not accept a view without any way to render it
                raise GrokError("View %r has no associated template or "
                                "'render' method." % factory, factory)

        # grab layer from class or module
        view_layer = determine_class_directive('grok.layer', factory, module_info, default=IDefaultBrowserLayer)

        view_name = util.class_annotation(factory, 'grok.name',
                                          factory_name)
        # __view_name__ is needed to support IAbsoluteURL on views
        factory.__view_name__ = view_name
        component.provideAdapter(factory,
                                 adapts=(view_context, view_layer),
                                 provides=interface.Interface,
                                 name=view_name)

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


class JSONGrokker(martian.ClassGrokker):
    component_class = grok.JSON

    def grok(self, name, factory, context, module_info, templates):
        view_context = util.determine_class_context(factory, context)
        methods = util.methods_from_class(factory)

        default_permission = get_default_permission(factory)

        for method in methods:
            # Create a new class with a __view_name__ attribute so the
            # JSON class knows what method to call.
            method_view = type(
                factory.__name__, (factory,),
                {'__view_name__': method.__name__}
                )
            component.provideAdapter(
                method_view, (view_context, IDefaultBrowserLayer),
                interface.Interface,
                name=method.__name__)

            # Protect method_view with either the permission that was
            # set on the method, the default permission from the class
            # level or zope.Public.

            permission = getattr(method, '__grok_require__',
                                 default_permission)
            make_checker(factory, method_view, permission)
        return True


class TraverserGrokker(martian.ClassGrokker):
    component_class = grok.Traverser

    def grok(self, name, factory, context, module_info, templates):
        factory_context = util.determine_class_context(factory, context)
        component.provideAdapter(factory,
                                 adapts=(factory_context, IBrowserRequest),
                                 provides=IBrowserPublisher)
        return True


class ModulePageTemplateGrokker(martian.InstanceGrokker):
    # this needs to happen before any other grokkers execute that actually
    # use the templates
    priority = 1000

    component_class = grok.PageTemplate

    def grok(self, name, instance, context, module_info, templates):
        templates.register(name, instance)
        instance._annotateGrokInfo(name, module_info.dotted_name)
        return True


class ModulePageTemplateFileGrokker(ModulePageTemplateGrokker):
    priority = 1000
    component_class = grok.PageTemplateFile


class FilesystemPageTemplateGrokker(martian.GlobalGrokker):
    # do this early on, but after ModulePageTemplateGrokker, as
    # findFilesystem depends on module-level templates to be
    # already grokked for error reporting
    priority = 999

    def grok(self, name, module, context, module_info, templates):
        templates.findFilesystem(module_info)
        return True


class SubscriberGrokker(martian.GlobalGrokker):

    def grok(self, name, module, context, module_info, templates):
        subscribers = module_info.getAnnotation('grok.subscribers', [])

        for factory, subscribed in subscribers:
            component.provideHandler(factory, adapts=subscribed)
            for iface in subscribed:
                zope.component.interface.provideInterface('', iface)
        return True


class AdapterDecoratorGrokker(martian.GlobalGrokker):

    def grok(self, name, module, context, module_info, templates):
        implementers = module_info.getAnnotation('implementers', [])
        for function in implementers:
            interfaces = getattr(function, '__component_adapts__', None)
            if interfaces is None:
                # There's no explicit interfaces defined, so we assume the
                # module context to be the thing adapted.
                util.check_context(module_info.getModule(), context)
                interfaces = (context, )
            component.provideAdapter(
                function, adapts=interfaces, provides=function.__implemented__)
        return True


class StaticResourcesGrokker(martian.GlobalGrokker):

    def grok(self, name, module, context, module_info, templates):
        # we're only interested in static resources if this module
        # happens to be a package
        if not module_info.isPackage():
            return False

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
        return True


class GlobalUtilityDirectiveGrokker(martian.GlobalGrokker):

    def grok(self, name, module, context, module_info, templates):
        infos = module_info.getAnnotation('grok.global_utility', [])

        for info in infos:
            if info.provides is None:
                util.check_implements_one(info.factory)
            if info.direct:
                obj = info.factory
            else:
                obj = info.factory()
            component.provideUtility(obj,
                                     provides=info.provides,
                                     name=info.name)
        return True


class SiteGrokker(martian.ClassGrokker):
    component_class = grok.Site
    priority = 500

    def grok(self, name, factory, context, module_info, templates):
        infos = util.class_annotation_list(factory, 'grok.local_utility', None)
        if infos is None:
            return False

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
                            "for utility registration of %r in site %r. "
                            "It implements an interface that is a specialization "
                            "of an interface implemented by grok.LocalUtility. "
                            "Specify the interface by either using grok.provides "
                            "on the utility or passing 'provides' to "
                            "grok.local_utility." % (info.factory, factory),
                            info.factory)
                else:
                    provides = list(interface.implementedBy(info.factory))

                util.check_implements_one_from_list(provides, info.factory)
                info.provides = provides[0]

        # raise an error in case of any duplicate registrations
        # on the class level (subclassing overrides, see below)
        used = set()
        class_infos = util.class_annotation(factory, 'grok.local_utility',
                                            [])
        for info in class_infos:
            key = (info.provides, info.name)
            if key in used:
                raise GrokError(
                    "Conflicting local utility registration %r in "
                    "site %r. Local utilities are registered multiple "
                    "times for interface %r and name %r." %
                    (info.factory, factory, info.provides, info.name),
                    factory)
            used.add(key)

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

        return True


def localUtilityRegistrationSubscriber(site, event):
    """A subscriber that fires to set up local utilities.
    """
    installed = getattr(site, '__grok_utilities_installed__', False)
    if installed:
        return

    for info in util.class_annotation(site.__class__,
                                      'grok.utilities_to_install', []):
        setupUtility(site, info.factory(), info.provides, name=info.name,
                     name_in_container=info.name_in_container,
                     public=info.public, setup=info.setup)

    # we are done. If this subscriber gets fired again, we therefore
    # do not register utilities anymore
    site.__grok_utilities_installed__ = True


def setupUtility(site, utility, provides, name=u'',
                 name_in_container=None, public=False, setup=None):
    """Set up a utility in a site.

    site - the site to set up the utility in
    utility - the utility to set up
    provides - the interface the utility should be registered with
    name - the name the utility should be registered under, default
      the empty string (no name)
    name_in_container - if given it will be used to add the utility
      object to its container. Otherwise a name will be made up
    public - if False, the utility will be stored in the site manager. If
      True, the utility will be storedin the site (it is assumed the
      site is a container)
    setup - if not None, it will be called with the utility as its first
       argument. This function can then be used to further set up the
       utility.
    """
    site_manager = site.getSiteManager()

    if not public:
        container = site_manager
    else:
        container = site

    if name_in_container is None:
        name_in_container = INameChooser(container).chooseName(
            utility.__class__.__name__, utility)
    container[name_in_container] = utility

    if setup is not None:
        setup(utility)

    site_manager.registerUtility(utility, provided=provides,
                                 name=name)

class DefinePermissionGrokker(martian.ClassGrokker):
    component_class = grok.Permission
    priority = 1500

    def grok(self, name, factory, context, module_info, templates):
        id = util.class_annotation(factory, 'grok.name', None)
        if id is None:
            raise GrokError(
                "A permission needs to have a dotted name for its id. Use "
                "grok.name to specify one.", factory)
        # We can safely convert to unicode, since the directives make sure
        # it is either unicode already or ASCII.
        id = unicode(id)
        permission = factory(
            id,
            unicode(util.class_annotation(factory, 'grok.title', id)),
            unicode(util.class_annotation(factory, 'grok.description', '')))
        component.provideUtility(permission, name=id)
        return True

class DefineRoleGrokker(martian.ClassGrokker):
    component_class = grok.Role
    priority = DefinePermissionGrokker.priority - 1

    def grok(self, name, factory, context, module_info, templates):
        id = util.class_annotation(factory, 'grok.name', None)
        if id is None:
            raise GrokError(
                "A role needs to have a dotted name for its id. Use "
                "grok.name to specify one.", factory)
        # We can safely convert to unicode, since the directives makes sure
        # it is either unicode already or ASCII.
        id = unicode(id)
        role = factory(
            id,
            unicode(util.class_annotation(factory, 'grok.title', id)),
            unicode(util.class_annotation(factory, 'grok.description', '')))
        component.provideUtility(role, name=id)
        permissions = util.class_annotation(factory, 'grok.permissions', ())
        for permission in permissions:
            rolePermissionManager.grantPermissionToRole(permission, id)
        return True

class AnnotationGrokker(martian.ClassGrokker):
    component_class = grok.Annotation

    def grok(self, name, factory, context, module_info, templates):
        adapter_context = util.determine_class_context(factory, context)
        provides = util.class_annotation(factory, 'grok.provides', None)
        if provides is None:
            base_interfaces = interface.implementedBy(grok.Annotation)
            factory_interfaces = interface.implementedBy(factory)
            real_interfaces = list(factory_interfaces - base_interfaces)
            util.check_implements_one_from_list(real_interfaces, factory)
            provides = real_interfaces[0]

        key = util.class_annotation(factory, 'grok.name', None)
        if key is None:
            key = factory.__module__ + '.' + factory.__name__

        @component.adapter(adapter_context)
        @interface.implementer(provides)
        def getAnnotation(context):
            annotations = IAnnotations(context)
            try:
                result = annotations[key]
            except KeyError:
                result = factory()
                annotations[key] = result

            # Containment has to be set up late to allow containment
            # proxies to be applied, if needed. This does not trigger
            # an event and is idempotent if containment is set up
            # already.
            contained_result = contained(result, context, key)
            return contained_result

        component.provideAdapter(getAnnotation)
        return True


class ApplicationGrokker(martian.ClassGrokker):
    component_class = grok.Application
    priority = 500

    def grok(self, name, factory, context, module_info, templates):
        # XXX fail loudly if the same application name is used twice.
        zope.component.provideUtility(factory,
                                      provides=grok.interfaces.IApplication,
                                      name='%s.%s' % (module_info.dotted_name,
                                                      name))
        return True


class IndexesGrokker(martian.InstanceGrokker):
    component_class = components.IndexesClass

    def grok(self, name, factory, context, module_info, templates):
        site = util.class_annotation(factory, 'grok.site', None)
        if site is None:
            raise GrokError("No site specified for grok.Indexes "
                            "subclass in module %r. "
                            "Use grok.site() to specify." % module_info.getModule(),
                            factory)
        indexes = util.class_annotation(factory, 'grok.indexes', None)
        if indexes is None:
            return False
        context = util.determine_class_context(factory, context)
        catalog_name = util.class_annotation(factory, 'grok.name', u'')
        zope.component.provideHandler(
            IndexesSetupSubscriber(catalog_name, indexes,
                                   context, module_info),
            adapts=(site,
                    grok.IObjectAddedEvent))
        return True


class IndexesSetupSubscriber(object):
    def __init__(self, catalog_name, indexes, context, module_info):
        self.catalog_name = catalog_name
        self.indexes = indexes
        self.context = context
        self.module_info = module_info

    def __call__(self, site, event):
        # make sure we have an intids
        self._createIntIds(site)
        # get the catalog
        catalog = self._createCatalog(site)
        # now install indexes
        for name, index in self.indexes.items():
            try:
                index.setup(catalog, name, self.context, self.module_info)
            except DuplicationError:
                raise GrokError(
                    "grok.Indexes in module %r causes "
                    "creation of catalog index %r in catalog %r, "
                    "but an index with that name is already present." %
                    (self.module_info.getModule(), name, self.catalog_name),
                    None)

    def _createCatalog(self, site):
        """Create the catalog if needed and return it.

        If the catalog already exists, return that.

        """
        catalog = zope.component.queryUtility(
            ICatalog, name=self.catalog_name, context=site, default=None)
        if catalog is not None:
            return catalog
        catalog = Catalog()
        setupUtility(site, catalog, ICatalog, name=self.catalog_name)
        return catalog

    def _createIntIds(self, site):
        """Create intids if needed, and return it.
        """
        intids = zope.component.queryUtility(
            IIntIds, context=site, default=None)
        if intids is not None:
            return intids
        intids = IntIds()
        setupUtility(site, intids, IIntIds)
        return intids


class I18nRegisterTranslationGrokker(martian.GlobalGrokker):
    
    def grok(self, name, factory, context, module_info, templates):
        dirslist = module_info.getAnnotation('grok.localesdir', [])
        set_default = not dirslist
        if not dirslist:
            # No localesdir explicitly declared in this module. Set a
            # default value.
            dirslist.append('locales')
        for localesdir in dirslist:
            abs_path = module_info.getResourcePath(localesdir)
            if not os.path.isdir(abs_path):
                if set_default:
                    # We silently ignore non-existing locale dirs,
                    # if their path was not set explicitly.
                    return False
                else:
                    raise GrokError(
                        "localesdir: directory %r declared in %r as "
                        "locales directory does not exist." % (
                        localesdir, module_info.dotted_name),
                        None)
            register_translations_directory(abs_path)
        return True


class SkinGrokker(martian.ClassGrokker):
    component_class = grok.Skin

    def grok(self, name, factory, context, module_info, templates):

        layer = determine_class_directive('grok.layer', factory, module_info, default=IBrowserRequest)
        name = grok.util.class_annotation(factory, 'grok.name', factory.__name__.lower())
        zope.component.interface.provideInterface(name, layer, IBrowserSkinType)
        return True


def determine_class_directive(directive_name, factory, module_info, default=None):
    directive = util.class_annotation(factory, directive_name, None)
    if directive is None:
        directive = module_info.getAnnotation(directive_name, None)
    if directive is not None:
        return directive
    else:
        return default

