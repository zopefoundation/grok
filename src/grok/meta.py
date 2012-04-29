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
