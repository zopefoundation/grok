#############################################################################
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
from zope.publisher.interfaces.http import IHTTPRequest

from zope.publisher.interfaces.xmlrpc import IXMLRPCRequest
from zope.viewlet.interfaces import IViewletManager, IViewlet
from zope.security.interfaces import IPermission
from zope.securitypolicy.interfaces import IRole
from zope.securitypolicy.rolepermission import rolePermissionManager

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
from grok import components, formlib, templatereg
from grok.util import check_permission, make_checker
from grok.interfaces import IRESTSkinType
from grok.interfaces import IViewletManager as IGrokViewletManager

from grokcore.component.scan import determine_module_component


def default_view_name(factory, module=None, **data):
    return factory.__name__.lower()

def default_fallback_to_name(factory, module, name, **data):
    return name

def default_annotation_provides(factory, module, **data):
    base_interfaces = interface.implementedBy(grok.Annotation)
    factory_interfaces = interface.implementedBy(factory)
    real_interfaces = list(factory_interfaces - base_interfaces)
    util.check_implements_one_from_list(real_interfaces, factory)
    return real_interfaces[0]

def default_annotation_name(factory, module, **data):
    return factory.__module__ + '.' + factory.__name__


class ViewletManagerContextGrokker(martian.GlobalGrokker):

    martian.priority(1001)

    def grok(self, name, module, module_info, config, **kw):
        viewletmanager = determine_module_component(module_info,
                                                    grok.viewletmanager,
                                                    IGrokViewletManager)
        grok.viewletmanager.set(module, viewletmanager)
        return True


class XMLRPCGrokker(martian.MethodGrokker):
    martian.component(grok.XMLRPC)
    martian.directive(grok.context)
    martian.directive(grok.require, name='permission')

    def execute(self, factory, method, config, context, permission, **kw):
        name = method.__name__

        # Make sure that the class inherits MethodPublisher, so that the
        # views have a location
        method_view = type(
            factory.__name__, (factory, MethodPublisher),
            {'__call__': method}
            )

        adapts = (context, IXMLRPCRequest)
        config.action(
            discriminator=('adapter', adapts, interface.Interface, name),
            callable=component.provideAdapter,
            args=(method_view, adapts, interface.Interface, name),
            )
        config.action(
            discriminator=('protectName', method_view, '__call__'),
            callable=make_checker,
            args=(factory, method_view, permission),
            )
        return True


class RESTGrokker(martian.MethodGrokker):
    martian.component(grok.REST)
    martian.directive(grok.context)
    martian.directive(grok.layer, default=grok.IRESTLayer)
    martian.directive(grok.require, name='permission')

    def execute(self, factory, method, config, permission, context, layer, **kw):
        name = method.__name__

        method_view = type(
            factory.__name__, (factory,),
            {'__call__': method }
            )

        adapts = (context, layer)
        config.action(
            discriminator=('adapter', adapts, interface.Interface, name),
            callable=component.provideAdapter,
            args=(method_view, adapts, interface.Interface, name),
            )
        config.action(
            discriminator=('protectName', method_view, '__call__'),
            callable=make_checker,
            args=(factory, method_view, permission),
            )
        return True


class ViewGrokker(martian.ClassGrokker):
    martian.component(grok.View)
    martian.directive(grok.context)
    martian.directive(grok.layer, default=IDefaultBrowserLayer)
    martian.directive(grok.name, get_default=default_view_name)
    martian.directive(grok.require, name='permission')

    def grok(self, name, factory, module_info, **kw):
        # Need to store the module info object on the view class so that it
        # can look up the 'static' resource directory.
        factory.module_info = module_info
        return super(ViewGrokker, self).grok(name, factory, module_info, **kw)

    def execute(self, factory, config, context, layer, name, permission, **kw):
        if util.check_subclass(factory, components.GrokForm):
            # setup form_fields from context class if we've encountered a form
            if getattr(factory, 'form_fields', None) is None:
                factory.form_fields = formlib.get_auto_fields(context)

            if not getattr(factory.render, 'base_method', False):
                raise GrokError(
                    "It is not allowed to specify a custom 'render' "
                    "method for form %r. Forms either use the default "
                    "template or a custom-supplied one." % factory,
                    factory)

        # find templates
        templates = factory.module_info.getAnnotation('grok.templates', None)
        if templates is not None:
            config.action(
                discriminator=None,
                callable=self.checkTemplates,
                args=(templates, factory.module_info, factory)
                )

        # safety belt: make sure that the programmer didn't use
        # @grok.require on any of the view's methods.
        methods = util.methods_from_class(factory)
        for method in methods:
            if grok.require.bind().get(method) is not None:
                raise GrokError('The @grok.require decorator is used for '
                                'method %r in view %r. It may only be used '
                                'for XML-RPC methods.'
                                % (method.__name__, factory), factory)

        # __view_name__ is needed to support IAbsoluteURL on views
        factory.__view_name__ = name
        adapts = (context, layer)

        config.action(
            discriminator=('adapter', adapts, interface.Interface, name),
            callable=component.provideAdapter,
            args=(factory, adapts, interface.Interface, name),
            )

        config.action(
            discriminator=('protectName', factory, '__call__'),
            callable=make_checker,
            args=(factory, factory, permission),
            )

        return True

    def checkTemplates(self, templates, module_info, factory):
        def has_render(factory):
            return (getattr(factory, 'render', None) and
                    not util.check_subclass(factory, grok.components.GrokForm))
        def has_no_render(factory):
            return not getattr(factory, 'render', None)
        templates.checkTemplates(module_info, factory, 'view',
                                 has_render, has_no_render)


class JSONGrokker(martian.MethodGrokker):
    martian.component(grok.JSON)
    martian.directive(grok.context)
    martian.directive(grok.require, name='permission')

    # TODO: this grokker doesn't support layers yet

    def execute(self, factory, method, config, context, permission, **kw):
        # Create a new class with a __view_name__ attribute so the
        # JSON class knows what method to call.
        method_view = type(
            factory.__name__, (factory,),
            {'__view_name__': method.__name__}
            )
        adapts = (context, IDefaultBrowserLayer)
        name = method.__name__

        config.action(
            discriminator=('adapter', adapts, interface.Interface, name),
            callable=component.provideAdapter,
            args=(method_view, adapts, interface.Interface, name),
            )
        config.action(
            discriminator=('protectName', method_view, '__call__'),
            callable=make_checker,
            args=(factory, method_view, permission),
            )
        return True


class TraverserGrokker(martian.ClassGrokker):
    martian.component(grok.Traverser)
    martian.directive(grok.context)

    def execute(self, factory, config, context, **kw):
        adapts = (context, IHTTPRequest)
        config.action(
            discriminator=('adapter', adapts, IBrowserPublisher, ''),
            callable=component.provideAdapter,
            args=(factory, adapts, IBrowserPublisher),
            )
        return True


class TemplateGrokker(martian.GlobalGrokker):
    # this needs to happen before any other grokkers execute that use
    # the template registry
    martian.priority(1001)

    def grok(self, name, module, module_info, config, **kw):
        module.__grok_templates__ = templatereg.TemplateRegistry()
        return True


class ModulePageTemplateGrokker(martian.InstanceGrokker):
    martian.component(grok.components.BaseTemplate)
    # this needs to happen before any other grokkers execute that actually
    # use the templates
    martian.priority(1000)
    
    def grok(self, name, instance, module_info, config, **kw):
        templates = module_info.getAnnotation('grok.templates', None)
        if templates is None:
            return False
        config.action(
            discriminator=None,
            callable=templates.register,
            args=(name, instance)
            )
        config.action(
            discriminator=None,
            callable=instance._annotateGrokInfo,
            args=(name, module_info.dotted_name)
            )
        return True


class FilesystemPageTemplateGrokker(martian.GlobalGrokker):
    # do this early on, but after ModulePageTemplateGrokker, as
    # findFilesystem depends on module-level templates to be
    # already grokked for error reporting
    martian.priority(999)

    def grok(self, name, module, module_info, config, **kw):
        templates = module_info.getAnnotation('grok.templates', None)
        if templates is None:
            return False
        config.action(
            discriminator=None,
            callable=templates.findFilesystem,
            args=(module_info,)
            )
        return True


class UnassociatedTemplatesGrokker(martian.GlobalGrokker):
    martian.priority(-1001)

    def grok(self, name, module, module_info, config, **kw):
        templates = module_info.getAnnotation('grok.templates', None)
        if templates is None:
            return False

        config.action(
            discriminator=None,
            callable=templates.checkUnassociated,
            args=(module_info,)
            )
        return True


class StaticResourcesGrokker(martian.GlobalGrokker):

    def grok(self, name, module, module_info, config, **kw):
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
        adapts = (IDefaultBrowserLayer,)
        provides = interface.Interface
        name = module_info.dotted_name
        config.action(
            discriminator=('adapter', adapts, provides, name),
            callable=component.provideAdapter,
            args=(resource_factory, adapts, provides, name),
            )
        return True


class SiteGrokker(martian.ClassGrokker):
    martian.component(grok.Site)
    martian.priority(500)
    martian.directive(grok.local_utility, name='infos')

    def execute(self, factory, config, infos, **kw):
        if not infos:
            return False

        infos = infos.values()
        for info in infos:
            if info.public and not IContainer.implementedBy(factory):
                raise GrokError(
                    "Cannot set public to True with grok.local_utility as "
                    "the site (%r) is not a container." %
                    factory, factory)

        # Store the list of info objects in their "natural" order on the
        # site class. They will be picked up by a subscriber doing the
        # actual registrations in definition order.
        factory.__grok_utilities_to_install__ = sorted(infos)
        adapts = (factory, grok.IObjectAddedEvent)

        config.action(
            discriminator=None,
            callable=component.provideHandler,
            args=(localUtilityRegistrationSubscriber, adapts),
            )
        return True


def localUtilityRegistrationSubscriber(site, event):
    """A subscriber that fires to set up local utilities.
    """
    installed = getattr(site, '__grok_utilities_installed__', False)
    if installed:
        return

    for info in getattr(site.__class__, '__grok_utilities_to_install__', []):
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


class PermissionGrokker(martian.ClassGrokker):
    martian.component(grok.Permission)
    martian.priority(1500)
    martian.directive(grok.name)
    martian.directive(grok.title, get_default=default_fallback_to_name)
    martian.directive(grok.description)

    def execute(self, factory, config, name, title, description, **kw):
        if not name:
            raise GrokError(
                "A permission needs to have a dotted name for its id. Use "
                "grok.name to specify one.", factory)
        # We can safely convert to unicode, since the directives make sure
        # it is either unicode already or ASCII.
        permission = factory(unicode(name), unicode(title),
                             unicode(description))

        config.action(
            discriminator=('utility', IPermission, name),
            callable=component.provideUtility,
            args=(permission, IPermission, name),
            order=-1 # need to do this early in the process
            )
        return True


class RoleGrokker(martian.ClassGrokker):
    martian.component(grok.Role)
    martian.priority(martian.priority.bind().get(PermissionGrokker()) - 1)
    martian.directive(grok.name)
    martian.directive(grok.title, get_default=default_fallback_to_name)
    martian.directive(grok.description)
    martian.directive(grok.permissions)

    def execute(self, factory, config, name, title, description,
                permissions, **kw):
        if not name:
            raise GrokError(
                "A role needs to have a dotted name for its id. Use "
                "grok.name to specify one.", factory)
        # We can safely convert to unicode, since the directives makes sure
        # it is either unicode already or ASCII.
        role = factory(unicode(name), unicode(title), unicode(description))

        config.action(
            discriminator=('utility', IRole, name),
            callable=component.provideUtility,
            args=(role, IRole, name),
            )

        for permission in permissions:
            config.action(
                discriminator=('grantPermissionToRole', permission, name),
                callable=rolePermissionManager.grantPermissionToRole,
                args=(permission, name),
                )
        return True


class AnnotationGrokker(martian.ClassGrokker):
    martian.component(grok.Annotation)
    martian.directive(grok.context, name='adapter_context')
    martian.directive(grok.provides, get_default=default_annotation_provides)
    martian.directive(grok.name, get_default=default_annotation_name)

    def execute(self, factory, config, adapter_context, provides, name, **kw):
        @component.adapter(adapter_context)
        @interface.implementer(provides)
        def getAnnotation(context):
            annotations = IAnnotations(context)
            try:
                result = annotations[name]
            except KeyError:
                result = factory()
                annotations[name] = result

            # Containment has to be set up late to allow containment
            # proxies to be applied, if needed. This does not trigger
            # an event and is idempotent if containment is set up
            # already.
            contained_result = contained(result, context, name)
            return contained_result

        config.action(
            discriminator=('adapter', adapter_context, provides, ''),
            callable=component.provideAdapter,
            args=(getAnnotation,),
            )
        return True


class ApplicationGrokker(martian.ClassGrokker):
    martian.component(grok.Application)
    martian.priority(500)

    def grok(self, name, factory, module_info, config, **kw):
        # XXX fail loudly if the same application name is used twice.
        provides = grok.interfaces.IApplication
        name = '%s.%s' % (module_info.dotted_name, name)
        config.action(
            discriminator=('utility', provides, name),
            callable=component.provideUtility,
            args=(factory, provides, name),
            )
        return True


class IndexesGrokker(martian.InstanceGrokker):
    martian.component(components.IndexesClass)

    def grok(self, name, factory, module_info, config, **kw):
        site = grok.site.bind().get(factory)
        context = grok.context.bind().get(factory, module_info.getModule())
        catalog_name = grok.name.bind().get(factory)

        if site is None:
            raise GrokError("No site specified for grok.Indexes "
                            "subclass in module %r. "
                            "Use grok.site() to specify."
                            % module_info.getModule(),
                            factory)
        indexes = getattr(factory, '__grok_indexes__', None)
        if indexes is None:
            return False

        subscriber = IndexesSetupSubscriber(catalog_name, indexes,
                                            context, module_info)
        subscribed = (site, grok.IObjectAddedEvent)
        config.action(
            discriminator=None,
            callable=component.provideHandler,
            args=(subscriber, subscribed),
            )
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


class SkinGrokker(martian.ClassGrokker):
    martian.component(grok.Skin)
    martian.directive(grok.layer, default=IBrowserRequest)
    martian.directive(grok.name, get_default=default_view_name)

    def execute(self, factory, config, name, layer, **kw):
        config.action(
            discriminator=('skin', name),
            callable=zope.component.interface.provideInterface,
            args=(name, layer, IBrowserSkinType)
            )
        return True

class RESTProtocolGrokker(martian.ClassGrokker):
    martian.component(grok.RESTProtocol)
    martian.directive(grok.layer, default=IBrowserRequest)
    martian.directive(grok.name, get_default=default_view_name)

    def execute(self, factory, config, name, layer, **kw):
        config.action(
            discriminator=('restprotocol', name),
            callable=zope.component.interface.provideInterface,
            args=(name, layer, IRESTSkinType)
            )
        return True

class ViewletManagerGrokker(martian.ClassGrokker):
    martian.component(grok.ViewletManager)
    martian.directive(grok.context)
    martian.directive(grok.layer, default=IDefaultBrowserLayer)
    martian.directive(grok.view)
    martian.directive(grok.name)

    def grok(self, name, factory, module_info, **kw):
        # Need to store the module info object on the view class so that it
        # can look up the 'static' resource directory.
        factory.module_info = module_info
        return super(ViewletManagerGrokker, self).grok(
            name, factory, module_info, **kw)

    def execute(self, factory, config, context, layer, view, name, **kw):
        # This will be used to support __name__ on the viewlet manager
        factory.__view_name__ = name

        # find templates
        templates = factory.module_info.getAnnotation('grok.templates', None)
        if templates is not None:
            config.action(
                discriminator=None,
                callable=self.checkTemplates,
                args=(templates, factory.module_info, factory)
                )

        config.action(
            discriminator = ('viewletManager', context, layer, view, name),
            callable = component.provideAdapter,
            args = (factory, (context, layer, view), IViewletManager, name)
            )
        return True

    def checkTemplates(self, templates, module_info, factory):
        def has_render(factory):
            return factory.render != grok.components.ViewletManager.render
        def has_no_render(factory):
            # always has a render method
            return False
        templates.checkTemplates(module_info, factory, 'viewlet manager',
                                 has_render, has_no_render)

class ViewletGrokker(martian.ClassGrokker):
    martian.component(grok.Viewlet)
    martian.directive(grok.context)
    martian.directive(grok.layer, default=IDefaultBrowserLayer)
    martian.directive(grok.view)
    martian.directive(grok.viewletmanager)
    martian.directive(grok.name, get_default=default_view_name)
    martian.directive(grok.require, name='permission')

    def grok(self, name, factory, module_info, **kw):
        # Need to store the module info object on the view class so that it
        # can look up the 'static' resource directory.
        factory.module_info = module_info
        return super(ViewletGrokker, self).grok(
            name, factory, module_info, **kw)

    def execute(self, factory, config,
                context, layer, view, viewletmanager, name, permission, **kw):
        # This will be used to support __name__ on the viewlet
        factory.__view_name__ = name

        # find templates
        templates = factory.module_info.getAnnotation('grok.templates', None)
        if templates is not None:
            config.action(
                discriminator=None,
                callable=self.checkTemplates,
                args=(templates, factory.module_info, factory)
                )

        config.action(
            discriminator = ('viewlet', context, layer,
                             view, viewletmanager, name),
            callable = component.provideAdapter,
            args = (factory, (context, layer, view, viewletmanager),
                    IViewlet, name)
            )

        config.action(
            discriminator=('protectName', factory, '__call__'),
            callable=make_checker,
            args=(factory, factory, permission, ['update', 'render']),
            )

        return True

    def checkTemplates(self, templates, module_info, factory):
        def has_render(factory):
            return factory.render != grok.components.Viewlet.render
        def has_no_render(factory):
            return not has_render(factory)
        templates.checkTemplates(module_info, factory, 'viewlet',
                                 has_render, has_no_render)
