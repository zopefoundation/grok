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
"""Grok interfaces
"""
from zope import interface
from zope.interface.interfaces import IInterface
from zope.publisher.interfaces.http import IHTTPRequest
from zope.app.container.interfaces import IContainer as IContainerBase

# Expose interfaces from grokcore.* packages as well:
import grokcore.component.interfaces
import grokcore.formlib.interfaces
import grokcore.security.interfaces
import grokcore.view.interfaces
import grokcore.viewlet.interfaces

from grokcore.component.interfaces import IContext
from grokcore.component.interfaces import IGrokErrors


class IGrokBaseClasses(grokcore.component.interfaces.IBaseClasses,
                       grokcore.security.interfaces.IBaseClasses,
                       grokcore.view.interfaces.IBaseClasses):
    Model = interface.Attribute("Base class for persistent content objects "
                                "(models).")
    Container = interface.Attribute("Base class for containers.")
    OrderedContainer = interface.Attribute("Base class for ordered containers.")
    Site = interface.Attribute("Mixin class for sites.")
    Application = interface.Attribute("Base class for applications.")
    Annotation = interface.Attribute("Base class for persistent annotations.")
    LocalUtility = interface.Attribute("Base class for local utilities.")
    XMLRPC = interface.Attribute("Base class for XML-RPC methods.")
    JSON = interface.Attribute("Base class for JSON methods.")
    REST = interface.Attribute("Base class for REST views.")
    Traverser = interface.Attribute("Base class for custom traversers.")
    Indexes = interface.Attribute("Base class for catalog index definitions.")
    Role = interface.Attribute("Base class for roles.")


class IGrokDirectives(grokcore.component.interfaces.IDirectives,
                      grokcore.security.interfaces.IDirectives,
                      grokcore.view.interfaces.IDirectives):

    def local_utility(factory, provides=None, name=u'',
                      setup=None, public=False, name_in_container=None):
        """Register a local utility.

        factory - the factory that creates the local utility
        provides - the interface the utility should be looked up with
        name - the name of the utility
        setup - a callable that receives the utility as its single argument,
                it is called after the utility has been created and stored
        public - if False, the utility will be stored below ++etc++site
                 if True, the utility will be stored directly in the site.
                 The site should in this case be a container.
        name_in_container - the name to use for storing the utility
        """

    def permissions(permissions):
        """Specify the permissions that comprise a role.
        """

    def site(class_or_interface):
        """Specifies the site that an indexes definition is for.

        It can only be used inside grok.Indexes subclasses.
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

class IGrokAPI(grokcore.security.interfaces.IGrokcoreSecurityAPI,
               grokcore.view.interfaces.IGrokcoreViewAPI,
               grokcore.viewlet.interfaces.IGrokcoreViewletAPI,
               grokcore.formlib.interfaces.IGrokcoreFormlibAPI,
               IGrokBaseClasses, IGrokDirectives,
               IGrokEvents, IGrokErrors):

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


    IRESTSkinType = interface.Attribute('The REST skin type')


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


class IREST(interface.Interface):
    context = interface.Attribute("Object that the REST handler presents.")

    request = interface.Attribute("Request that REST handler was looked"
                                  "up with.")

    body = interface.Attribute(
        """The text of the request body.""")

class IApplication(interface.Interface):
    """Marker-interface for grok application factories.

    Used to register applications as utilities to look them up and
    provide a list of grokked applications.
    """

class IIndexDefinition(interface.Interface):
    """Define an index for grok.Indexes.
    """

    def setup(catalog, name, context):
        """Set up index called name in given catalog.

        Use name for index name and attribute to index. Set up
        index for interface or class context.
        """

class IRESTLayer(IHTTPRequest):
    """REST-specific Request functionality.

    Base Interfaces for defining REST-layers.
    """

class IRESTSkinType(IInterface):
    """Skin type for REST requests.
    """

class IContainer(IContext, IContainerBase):
    """A Grok container.
    """

class IGrokSecurityView(interface.Interface):
    """A view treated special by the Grok publisher.

    Views that provide this interface are treated more generously by
    the Grok publisher, as they are allowed to use attributes, which
    are not covered by permission setttings.

    `grok.Permission` and `grok.require` settings however, will be
    applied to such views.
    """
