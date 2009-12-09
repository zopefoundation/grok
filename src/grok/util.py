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
"""Grok utility functions.
"""
import grok
import grok.interfaces
import zope.event
import zope.location.location
from zope import interface
from zope.schema.interfaces import WrongType
from zope.exceptions.interfaces import DuplicationError
from zope.security.checker import NamesChecker, defineChecker

from grokcore.view.util import url
from grokcore.security.util import check_permission

def make_checker(factory, view_factory, permission, method_names=None):
    """Make a checker for a view_factory associated with factory.

    These could be one and the same for normal views, or different
    in case we make method-based views such as for JSON and XMLRPC.
    """
    if method_names is None:
        method_names = ['__call__']
    if permission is not None:
        check_permission(factory, permission)
    if permission is None or permission == 'zope.Public':
        checker = NamesChecker(method_names)
    else:
        checker = NamesChecker(method_names, permission)
    defineChecker(view_factory, checker)


def safely_locate_maybe(obj, parent, name):
    """Set an object's __parent__ (and __name__) if the object's
    __parent__ attribute doesn't exist yet or is None.

    If the object provides ILocation, __parent__ and __name__ will be
    set directly.  A location proxy will be returned otherwise.
    """
    if getattr(obj, '__parent__', None) is not None:
        return obj
    # This either sets __parent__ or wraps 'obj' in a LocationProxy
    return zope.location.location.located(obj, parent, name)


def applySkin(request, skin, skin_type):
    """Change the presentation skin for this request.
    """
    # Remove all existing skin declarations (commonly the default skin).
    ifaces = [iface for iface in interface.directlyProvidedBy(request)
              if not skin_type.providedBy(iface)]
    # Add the new skin.
    ifaces.append(skin)
    interface.directlyProvides(request, *ifaces)

def getApplication():
    """Return the nearest enclosing `grok.Application`.

    Raises ValueError if no Application can be found.
    """
    site = grok.getSite()
    if grok.interfaces.IApplication.providedBy(site):
        return site
    # Another sub-site is within the application. Walk up the object
    # tree until we get to the an application.
    obj = site
    while obj is not None:
        if isinstance(obj, grok.Application):
            return obj
        obj = obj.__parent__
    raise ValueError("No application found.")

def application_url(request, obj, name=None, data={}):
    """Return the URL of the nearest enclosing `grok.Application`.

    Raises ValueError if no Application can be found.
    """
    return url(request, getApplication(), name, data)

def create_application(factory, container, name):
    """Creates an application and triggers the events from
    the application lifecycle.
    """
    # Check the factory.
    if not grok.interfaces.IApplication.implementedBy(factory):
        raise WrongType(factory)

    # Check the availability of the name in the container.
    if name in container:
        raise DuplicationError(name)

    # Instanciate the application
    application = factory()

    # Trigger the creation event.
    grok.notify(grok.ObjectCreatedEvent(application))

    # Persist the application.
    # This may raise a DuplicationError.
    container[name] = application

    # Trigger the initialization event.
    grok.notify(grok.ApplicationInitializedEvent(application))

    return application
