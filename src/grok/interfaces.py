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
from zope.interface.interfaces import IInterface
from zope.component.interfaces import IObjectEvent
from zope.publisher.interfaces.http import IHTTPRequest
from zope.container.interfaces import IContainer as IContainerBase

# Expose interfaces from grokcore.* packages as well:
import grokcore.annotation.interfaces
import grokcore.component.interfaces
import grokcore.formlib.interfaces
import grokcore.layout.interfaces
import grokcore.json.interfaces
import grokcore.security.interfaces
import grokcore.rest.interfaces
import grokcore.site.interfaces
import grokcore.view.interfaces
import grokcore.viewlet.interfaces
import grokcore.xmlrpc.interfaces
import grokcore.traverser.interfaces

from grokcore.component.interfaces import IContext
from grokcore.component.interfaces import IGrokErrors

from grokcore.rest.interfaces import IREST, IRESTSkinType, IRESTLayer

class IGrokBaseClasses(grokcore.annotation.interfaces.IBaseClasses,
                       grokcore.component.interfaces.IBaseClasses,
                       grokcore.security.interfaces.IBaseClasses,
                       grokcore.rest.interfaces.IBaseClasses,
                       grokcore.site.interfaces.IBaseClasses,
                       grokcore.view.interfaces.IBaseClasses,
                       grokcore.json.interfaces.IBaseClasses,
                       grokcore.layout.interfaces.IBaseClasses,
                       grokcore.traverser.interfaces.IBaseClasses,
                       grokcore.xmlrpc.interfaces.IBaseClasses):
    Model = interface.Attribute(
        "Base class for persistent content objects (models).")
    Container = interface.Attribute("Base class for containers.")
    OrderedContainer = interface.Attribute("Base class for ordered containers.")
    Application = interface.Attribute("Base class for applications.")
    View = interface.Attribute("Base class views.")
    ExceptionView = interface.Attribute("Base class for excetion views.")
    NotFoundView = interface.Attribute("Base class notfound exception views.")
    UnauthorizedView = interface.Attribute(
        "Base class unauthorized exception views.")
    Role = interface.Attribute("Base class for roles.")


class IGrokDirectives(grokcore.component.interfaces.IDirectives,
                      grokcore.security.interfaces.IDirectives,
                      grokcore.site.interfaces.IDirectives,
                      grokcore.view.interfaces.IDirectives):

    def permissions(permissions):
        """Specify the permissions that comprise a role.
        """


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

    IApplicationInitializedEvent = interface.Attribute("")

    ApplicationInitializedEvent = interface.Attribute("")


class IGrokAPI(grokcore.component.interfaces.IGrokcoreComponentAPI,
               grokcore.formlib.interfaces.IGrokcoreFormlibAPI,
               grokcore.layout.interfaces.IGrokcoreLayoutAPI,
               grokcore.security.interfaces.IGrokcoreSecurityAPI,
               grokcore.site.interfaces.IGrokcoreSiteAPI,
               grokcore.view.interfaces.IGrokcoreViewAPI,
               grokcore.viewlet.interfaces.IGrokcoreViewletAPI,
               IGrokBaseClasses,
               IGrokDirectives,
               IGrokErrors,
               IGrokEvents):

    # BBB this is deprecated
    def grok(dotted_name):
        """Grok a module or package specified by ``dotted_name``.

        NOTE: This function will be removed from the public Grok
        public API.  For tests and interpreter sessions, use
        grok.testing.grok().
        """

    # BBB this is deprecated
    def grok_component(name, component, context=None, module_info=None,
                       templates=None):
        """Grok an arbitrary object. Can be useful during testing.

        name - the name of the component (class name, or global instance name
               as it would appear in a module).
        component - the object (class, etc) to grok.
        context - the context object (optional).
        module_info - the module being grokked (optional).
        templates - the templates registry (optional).

        Note that context, module_info and templates might be required
        for some grokkers which rely on them.

        NOTE: This function will be removed from the public Grok
        public API.  For tests and interpreter sessions, use
        grok.testing.grok_component().
        """

    def notify(event):
        """Send ``event`` to event subscribers."""

    def getSite():
        """Get the current site."""

    # XXX should be moved to the respective API declarations!
    IRESTSkinType = interface.Attribute('The REST skin type')
    IApplication = interface.Attribute('The application model interface')


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


class IIndexDefinition(interface.Interface):
    """Define an index for grok.Indexes.
    """

    def setup(catalog, name, context):
        """Set up index called name in given catalog.

        Use name for index name and attribute to index. Set up
        index for interface or class context.
        """


class IContainer(IContext, IContainerBase):
    """A Grok container.
    """
