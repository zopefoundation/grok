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
from zope import interface, schema
from zope.formlib.interfaces import reConstraint
from zope.interface.interfaces import IInterface
from zope.viewlet.interfaces import IViewletManager as IViewletManagerBase
from zope.app.container.interfaces import IContainer as IContainerBase

import grokcore.component.interfaces
import grokcore.security.interfaces
import grokcore.view.interfaces

# Expose interfaces from grokcore.* packages as well:
from grokcore.component.interfaces import IContext
from grokcore.component.interfaces import IGrokErrors
from grokcore.view.interfaces import ITemplateFileFactory
from grokcore.view.interfaces import ITemplate


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
    Form = interface.Attribute("Base class for forms.")
    AddForm = interface.Attribute("Base class for add forms.")
    EditForm = interface.Attribute("Base class for edit forms.")
    DisplayForm = interface.Attribute("Base class for display forms.")
    Indexes = interface.Attribute("Base class for catalog index definitions.")
    ViewletManager = interface.Attribute("Base class for viewletmanager.")
    Viewlet = interface.Attribute("Base class for viewlet.")
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

    def order(value=None):
        """Control the ordering of components.

        If the value is specified, the order will be determined by sorting on
        it.
        If no value is specified, the order will be determined by definition
        order within the module.
        If the directive is absent, the order will be determined by class name.
        (unfortunately our preferred default behavior on absence which would
        be like grok.order() without argument is hard to implement in Python)

        Inter-module order is by dotted name of the module the
        components are in; unless an explicit argument is specified to
        ``grok.order()``, components are grouped by module.

        The function grok.util.sort_components can be used to sort
        components according to these rules.
        """


class IGrokDecorators(grokcore.component.interfaces.IDecorators):

    def action(label, **options):
        """Decorator that defines an action factory based on a form
        method. The method receives the form data as keyword
        parameters."""


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


class IGrokAPI(grokcore.security.interfaces.IGrokcoreSecurityAPI,
               grokcore.view.interfaces.IGrokcoreViewAPI,
               IGrokBaseClasses, IGrokDirectives, IGrokDecorators,
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

    def Fields(*args, **kw):
        """Return a list of formlib fields based on interfaces and/or schema
        fields."""

    def AutoFields(context):
        """Return a list of fields for context autogenerated by grok.
        """

    def action(label, actions=None, **options):
        """grok-specific action decorator.
        """

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


class IGrokForm(IGrokView):
    """Grok form API, inspired by zope.formlib's IFormBaseCustomization.

    We explicitly don't inherit from IFormBaseCustomization because
    that would imply ISubPage with another definition of update() and
    render() than IGrokView has.
    """

    prefix = schema.ASCII(
        constraint=reConstraint(
            '[a-zA-Z][a-zA-Z0-9_]*([.][a-zA-Z][a-zA-Z0-9_]*)*',
            "Must be a sequence of not-separated identifiers"),
        description=u"""Page-element prefix

        All named or identified page elements in a subpage should have
        names and identifiers that begin with a subpage prefix
        followed by a dot.
        """,
        readonly=True,
        )

    def setPrefix(prefix):
        """Update the subpage prefix
        """

    label = interface.Attribute("A label to display at the top of a form")

    status = interface.Attribute(
        """An update status message

        This is normally generated by success or failure handlers.
        """)

    errors = interface.Attribute(
        """Sequence of errors encountered during validation
        """)

    form_result = interface.Attribute(
        """Return from action result method
        """)

    form_reset = interface.Attribute(
        """Boolean indicating whether the form needs to be reset
        """)

    form_fields = interface.Attribute(
        """The form's form field definitions

        This attribute is used by many of the default methods.
        """)

    widgets = interface.Attribute(
        """The form's widgets

        - set by setUpWidgets

        - used by validate
        """)

    def setUpWidgets(ignore_request=False):
        """Set up the form's widgets.

        The default implementation uses the form definitions in the
        form_fields attribute and setUpInputWidgets.

        The function should set the widgets attribute.
        """

    def validate(action, data):
        """The default form validator

        If an action is submitted and the action doesn't have it's own
        validator then this function will be called.
        """

    template = interface.Attribute(
        """Template used to display the form
        """)

    def resetForm():
        """Reset any cached data because underlying content may have changed
        """

    def error_views():
        """Return views of any errors.

        The errors are returned as an iterable.
        """

    def applyData(obj, **data):
        """Save form data to an object.

        This returns a dictionary with interfaces as keys and lists of
        field names as values to indicate which fields in which
        schemas had to be changed in order to save the data.  In case
        the method works in update mode (e.g. on EditForms) and
        doesn't have to update an object, the dictionary is empty.
        """

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

class IRESTSkinType(IInterface):
    """Skin type for REST requests.
    """

class IContainer(IContext, IContainerBase):
    """A Grok container.
    """

class IViewletManager(IViewletManagerBase):
    """The Grok viewlet manager.
    """
