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
"""Grokkers for Grok-configured components.

This `meta` module contains the actual grokker mechanisms for which the
Grok web framework is named.  A directive in the adjacent `meta.zcml`
file directs the `martian` library to scan this file, where it discovers
and registers the grokkers you see below.  The grokkers are then active
and available as `martian` recursively examines the packages and modules
of a Grok-based web application.

"""
import zope.component.interface
from zope import interface, component
from zope.interface.interface import InterfaceClass
from zope.publisher.interfaces.browser import (IDefaultBrowserLayer,
                                               IBrowserPublisher)
from zope.publisher.interfaces.http import IHTTPRequest

from zope.publisher.interfaces.xmlrpc import IXMLRPCRequest
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
from grok import components
from grok.util import make_checker
from grok.interfaces import IRESTSkinType

from grokcore.security.meta import PermissionGrokker

from grokcore.view.meta.views import default_fallback_to_name


def default_annotation_provides(factory, module, **data):
    base_interfaces = interface.implementedBy(grok.Annotation)
    factory_interfaces = interface.implementedBy(factory)
    real_interfaces = list(factory_interfaces - base_interfaces)
    util.check_implements_one_from_list(real_interfaces, factory)
    return real_interfaces[0]

def default_annotation_name(factory, module, **data):
    return factory.__module__ + '.' + factory.__name__


class XMLRPCGrokker(martian.MethodGrokker):
    """Grokker for methods of a `grok.XMLRPC` subclass.

    When an application defines a `grok.XMLRPC` view, we do not actually
    register the view with the Component Architecture.  Instead, we grok
    each of its methods separately, placing them each inside of a new
    class that we create on-the-fly by calling `type()`.  We make each
    method the `__call__()` method of its new class, since that is how
    Zope always invokes views.  And it is this new class that is then
    made the object of the two configuration actions that we schedule:
    one to activate it as an XML-RPC adapter for the context, and the
    other to prepare a security check for the adapter.

    """
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
    """Grokker for methods of a `grok.REST` subclass.

    When an application defines a `grok.REST` view, we do not actually
    register the view with the Component Architecture.  Instead, we grok
    each of its methods separately, placing them each inside of a new
    class that we create on-the-fly by calling `type()`.  We make each
    method the `__call__()` method of its new class, since that is how
    Zope always invokes views.  And it is this new class that is then
    made the object of the two configuration actions that we schedule:
    one to activate it as a REST adapter for the context, and the other
    to prepare a security check for the adapter.

    This results in several registered views, typically with names like
    `GET`, `PUT`, and `POST` - one for each method that the `grok.REST`
    subclass defines.

    """
    martian.component(grok.REST)
    martian.directive(grok.context)
    martian.directive(grok.layer, default=grok.IRESTLayer)
    martian.directive(grok.require, name='permission')

    def execute(self, factory, method, config, permission, context,
                layer, **kw):
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


_restskin_not_used = object()

class RestskinInterfaceDirectiveGrokker(martian.InstanceGrokker):
    """Grokker for interfaces providing the `grok.restskin()` directive.

    Applications create REST skins by subclassing `grok.IRESTLayer`
    and providing the subclass with a `grok.restskin()` directive giving
    the prefix string which distinguishes that REST layers from others.
    This grokker registers those skins.

    """
    martian.component(InterfaceClass)

    def grok(self, name, interface, module_info, config, **kw):
        # This `InstanceGrokker` will be called for every instance of
        # `InterfaceClass` - that is, for every interface defined in an
        # application module!  So we have to do our own filtering, by
        # checking whether each interface includes the `grok.restskin()`
        # directive, and skipping those that do not.
        restskin = grok.restskin.bind(default=_restskin_not_used
                                      ).get(interface)
        if restskin is _restskin_not_used:
            # The restskin directive is not actually used on the found
            # interface.
            return False

        if not interface.extends(grok.IRESTLayer):
            # For REST layers it is required to extend IRESTLayer.
            raise GrokError(
                "The grok.restskin() directive is used on interface %r. "
                "However, %r does not extend IRESTLayer which is "
                "required for interfaces that are used as layers and are to "
                "be registered as a restskin."
                % (interface.__identifier__, interface.__identifier__),
                interface
                )
        config.action(
            discriminator=('restprotocol', restskin),
            callable=zope.component.interface.provideInterface,
            args=(restskin, interface, IRESTSkinType)
            )
        return True


class JSONGrokker(martian.MethodGrokker):
    """Grokker for methods of a `grok.JSON` subclass.

    When an application defines a `grok.JSON` view, we do not actually
    register the view with the Component Architecture.  Instead, we grok
    each of its methods separately, placing them each inside of a new
    class that we create on-the-fly by calling `type()`.  We make each
    method the `__call__()` method of its new class, since that is how
    Zope always invokes views.  And it is this new class that is then
    made the object of the two configuration actions that we schedule:
    one to activate it as a JSON adapter for the context, and the other
    to prepare a security check for the adapter.

    """
    martian.component(grok.JSON)
    martian.directive(grok.context)
    martian.directive(grok.require, name='permission')
    martian.directive(grok.layer, default=IDefaultBrowserLayer)

    def execute(
            self, factory, method, config, context, permission, layer, **kw):
        # Create a new class with a __view_name__ attribute so the
        # JSON class knows what method to call.
        method_view = type(
            factory.__name__, (factory,),
            {'__view_name__': method.__name__}
            )
        adapts = (context, layer)
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
    """Grokker for subclasses of `grok.Traverser`."""
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


class SiteGrokker(martian.ClassGrokker):
    """Grokker for subclasses of `grok.Site`."""
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


class RoleGrokker(martian.ClassGrokker):
    """Grokker for components subclassed from `grok.Role`.

    Each role is registered as a global utility providing the service
    `IRole` under its own particular name, and then granted every
    permission named in its `grok.permission()` directive.

    """
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
    """Grokker for components subclassed from `grok.Annotation`."""
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
    """Grokker for Grok application classes."""
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
    """Grokker for Grok index bundles."""
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
    """Helper that sets up indexes when their Grok site is created.

    Each `grok.Indexes` class serves as an assertion that, whenever an
    instance of its `grok.site()` is created, the given list of indexes
    should be generated as well.  But a long period of time could elapse
    between when the application starts (and its indexes are grokked),
    and the moment, maybe days or weeks later, when a new instance of
    that `grok.Site` is created.  Hence this `IndexesSetupSubscriber`:
    it can be instantiated at grokking time with the index information,
    and then registered with the Component Architecture as an event that
    should be fired later, whenever the right kind of `grok.Site` is
    instantiated.  At that point its `__call__` method is kicked off and
    it makes sure the index catalogs get created properly.

    """
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

