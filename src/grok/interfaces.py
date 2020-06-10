##############################################################################
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
"""Grok interfaces
"""
from zope import interface
from zope.interface.interfaces import IObjectEvent
from zope.container.interfaces import IContainer as IContainerBase

# Expose interfaces from grokcore.* packages as well:
import grokcore.annotation.interfaces
import grokcore.catalog.interfaces
import grokcore.component.interfaces
import grokcore.formlib.interfaces
import grokcore.json.interfaces
import grokcore.layout.interfaces
import grokcore.rest.interfaces
import grokcore.security.interfaces
import grokcore.site.interfaces
import grokcore.traverser.interfaces
import grokcore.view.interfaces
import grokcore.viewlet.interfaces
import grokcore.xmlrpc.interfaces

from grokcore.component.interfaces import IContext
from grokcore.component.interfaces import IGrokErrors

from grokcore.rest.interfaces import IREST  # noqa: F401
from grokcore.rest.interfaces import IRESTSkinType  # noqa: F401
from grokcore.rest.interfaces import IRESTLayer  # noqa: F401


class IGrokBaseClasses(
        grokcore.annotation.interfaces.IBaseClasses,
        grokcore.catalog.interfaces.IBaseClasses,
        grokcore.component.interfaces.IBaseClasses,
        grokcore.json.interfaces.IBaseClasses,
        grokcore.layout.interfaces.IBaseClasses,
        grokcore.rest.interfaces.IBaseClasses,
        grokcore.security.interfaces.IBaseClasses,
        grokcore.site.interfaces.IBaseClasses,
        grokcore.traverser.interfaces.IBaseClasses,
        grokcore.view.interfaces.IBaseClasses,
        grokcore.xmlrpc.interfaces.IBaseClasses):

    Container = interface.Attribute(
        "Base class for containers.")

    ExceptionView = interface.Attribute(
        "Base class for excetion views.")

    Model = interface.Attribute(
        "Base class for persistent content objects (models).")

    NotFoundView = interface.Attribute(
        "Base class notfound exception views.")

    OrderedContainer = interface.Attribute(
        "Base class for ordered containers.")

    UnauthorizedView = interface.Attribute(
        "Base class unauthorized exception views.")

    View = interface.Attribute(
        "Base class views.")


class IGrokDirectives(
        grokcore.component.interfaces.IDirectives,
        grokcore.security.interfaces.IDirectives,
        grokcore.site.interfaces.IDirectives,
        grokcore.view.interfaces.IDirectives):
    pass


class IGrokEvents(interface.Interface):

    IObjectCreatedEvent = interface.Attribute("")

    ObjectCreatedEvent = interface.Attribute("")

    IObjectModifiedEvent = interface.Attribute("")

    ObjectModifiedEvent = interface.Attribute("")

    IObjectCopiedEvent = interface.Attribute("")

    ObjectCopiedEvent = interface.Attribute("")

    IObjectAddedEvent = interface.Attribute("")

    ObjectAddedEvent = interface.Attribute("")

    IObjectMovedEvent = interface.Attribute("")

    ObjectMovedEvent = interface.Attribute("")

    IObjectRemovedEvent = interface.Attribute("")

    ObjectRemovedEvent = interface.Attribute("")

    IContainerModifiedEvent = interface.Attribute("")

    ContainerModifiedEvent = interface.Attribute("")

    IBeforeTraverseEvent = interface.Attribute("")

    IApplicationAddedEvent = interface.Attribute("")

    ApplicationAddedEvent = interface.Attribute("")


class IGrokAPI(
        grokcore.component.interfaces.IGrokcoreComponentAPI,
        grokcore.formlib.interfaces.IGrokcoreFormlibAPI,
        grokcore.layout.interfaces.IGrokcoreLayoutAPI,
        grokcore.security.interfaces.IGrokcoreSecurityAPI,
        grokcore.site.interfaces.IGrokcoreSiteAPI,
        grokcore.view.interfaces.IGrokcoreViewAPI,
        grokcore.rest.interfaces.IGrokcoreRestAPI,
        grokcore.viewlet.interfaces.IGrokcoreViewletAPI,
        IGrokBaseClasses,
        IGrokDirectives,
        IGrokErrors,
        IGrokEvents):

    def notify(event):
        """Send ``event`` to event subscribers."""

    def create_application(factory, folder, name):
        """Create and add a new Grok application to the given folder under
        name.
        """


class IGrokView(grokcore.view.interfaces.IGrokView):
    """Grok views all provide this interface."""

    def application_url(name=None):
        """Return the URL of the closest application object in the
        hierarchy or the URL of a named object (``name`` parameter)
        relative to the closest application object.
        """

    def flash(message, type='message'):
        """Send a short message to the user."""


class IGrokForm(grokcore.formlib.interfaces.IGrokForm, IGrokView):
    """All Grok forms provides this interface."""


class IContainer(IContext, IContainerBase):
    """A Grok container.
    """


class IDatabaseCreatedEvent(IObjectEvent):
    """Event triggered the first time the database is created. It is only
    triggered one time and can be used to add new applications or
    utilities in the root of it.

    """
