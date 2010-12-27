#############################################################################
#
# Copyright (c) 2006-2007 Zope Foundation and Contributors.
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
from zope.publisher.interfaces.browser import IBrowserPublisher
from zope.publisher.interfaces.http import IHTTPRequest

from zope.publisher.interfaces.xmlrpc import IXMLRPCRequest
from zope.securitypolicy.interfaces import IRole
from zope.securitypolicy.rolepermission import rolePermissionManager

from zope.i18nmessageid import Message
from zope.intid import IntIds
from zope.intid.interfaces import IIntIds
from zope.catalog.catalog import Catalog
from zope.catalog.interfaces import ICatalog
from zope.location import Location
from zope.exceptions.interfaces import DuplicationError
from zope.publisher.xmlrpc import XMLRPCView

import martian
from martian.error import GrokError

import grok
from grok import components
from grok.interfaces import IRESTSkinType

import grokcore.site.interfaces
from grokcore.security.meta import PermissionGrokker

from grokcore.view import make_checker


def default_fallback_to_name(factory, module, name, **data):
    return name


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
        if not isinstance(title, Message):
            title = unicode(title)
        if not isinstance(description, Message):
            description = unicode(description)
        role = factory(unicode(name), title, description)

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


class ApplicationGrokker(martian.ClassGrokker):
    """Grokker for Grok application classes."""
    martian.component(grok.Application)
    martian.priority(500)

    def grok(self, name, factory, module_info, config, **kw):
        # XXX fail loudly if the same application name is used twice.
        provides = grokcore.site.interfaces.IApplication
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
        setupUtility = component.getUtility(
            grokcore.site.interfaces.IUtilityInstaller)
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
        setupUtility = component.getUtility(
            grokcore.site.interfaces.IUtilityInstaller)
        setupUtility(site, intids, IIntIds)
        return intids
