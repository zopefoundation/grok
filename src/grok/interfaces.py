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
from zope.publisher.interfaces.browser import IBrowserPage
from zope.formlib.interfaces import reConstraint

class IGrokBaseClasses(interface.Interface):
    ClassGrokker = interface.Attribute("Base class to define a class "
                                       "grokker.")
    InstanceGrokker = interface.Attribute("Base class to define an "
                                          "instance grokker.")
    ModuleGrokker = interface.Attribute("Base class to define a "
                                        "module grokker.")
    Model = interface.Attribute("Base class for persistent content objects "
                                "(models).")
    Container = interface.Attribute("Base class for containers.")
    Site = interface.Attribute("Mixin class for sites.")
    Application = interface.Attribute("Base class for applications.")
    Adapter = interface.Attribute("Base class for adapters.")
    MultiAdapter = interface.Attribute("Base class for multi-adapters.")
    Annotation = interface.Attribute("Base class for persistent annotations.")
    GlobalUtility = interface.Attribute("Base class for global utilities.")
    LocalUtility = interface.Attribute("Base class for local utilities.")
    View = interface.Attribute("Base class for browser views.")
    XMLRPC = interface.Attribute("Base class for XML-RPC methods.")
    Traverser = interface.Attribute("Base class for custom traversers.")
    Form = interface.Attribute("Base class for forms.")
    AddForm = interface.Attribute("Base class for add forms.")
    EditForm = interface.Attribute("Base class for edit forms.")
    DisplayForm = interface.Attribute("Base class for display forms.")
    Indexes = interface.Attribute("Base class for catalog index definitions.")
    Layer = interface.Attribute("Base interface for layers.")
    Skin = interface.Attribute("Base class for skin.")


class IGrokErrors(interface.Interface):

    def GrokError(message, component):
        """Error indicating that a problem occurrend during the
        grokking of a module (at "grok time")."""

    def GrokImportError(*args):
        """Error indicating a problem at import time."""


class IGrokDirectives(interface.Interface):

    def implements(*interfaces):
        """Declare that a class implements the given interfaces."""

    def adapts(*classes_or_interfaces):
        """Declare that a class adapts objects of the given classes or
        interfaces."""

    def context(class_or_interface):
        """Declare the context for views, adapters, etc.

        This directive can be used on module and class level.  When
        used on module level, it will set the context for all views,
        adapters, etc. in that module.  When used on class level, it
        will set the context for that particular class."""

    def name(name):
        """Declare the name of a view or adapter/multi-adapter.

        This directive can only be used on class level."""

    def layer(layer):
        """Declare the layer for the view.

        This directive acts as a contraint on the 'request' of
        grok.View. This directive can only be used on class level."""

    def skin(skin):
        """Declare this layer as a named skin.

        This directive can only be used on class level."""

    def template(template):
        """Declare the template name for a view.

        This directive can only be used on class level."""

    def templatedir(directory):
        """Declare a directory to be searched for templates.

        By default, grok will take the name of the module as the name
        of the directory.  This can be overridden using
        ``templatedir``."""

    def localesdir(directory):
        """Register translations in a directory.

        By default, grok will look for a directory ``locales`` in the
        package of a module and - if found - try to register
        translations in it.

        The name of the directory or additional directories can be
        declared using ``localesdir``.
        """

    def provides(interface):
        """Explicitly specify with which interface a component will be
        looked up."""

    def baseclass():
        """Mark this class as a base class.

        This means it won't be grokked, though if it's a possible context,
        it can still serve as a context.
        """

    def global_utility(factory, provides=None, name=u''):
        """Register a global utility.

        factory - the factory that creates the global utility
        provides - the interface the utility should be looked up with
        name - the name of the utility
        """

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

    def require(permission):
        """Protect a view class or an XMLRPC method with ``permision``.

        ``permission`` must already be defined, e.g. using
        grok.Permission.

        grok.require can be used as a class-level directive or as a
        method decorator."""

    def site(class_or_interface):
        """Specifies the site that an indexes definition is for.

        It can only be used inside grok.Indexes subclasses.
        """


class IGrokDecorators(interface.Interface):

    def subscribe(*classes_or_interfaces):
        """Declare that a function subscribes to an event or a
        combination of objects and events."""

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


class IGrokAPI(IGrokBaseClasses, IGrokDirectives, IGrokDecorators,
               IGrokEvents, IGrokErrors):

    def grok(dotted_name):
        """Grok a module or package specified by ``dotted_name``."""

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
        """

    def url(request, obj, name=None):
        """Generate the URL to an object with optional name attached.
        """

    def notify(event):
        """Send ``event`` to event subscribers."""

    def getSite():
        """Get the current site."""

    def PageTemplate(template):
        """Create a Grok PageTemplate object from ``template`` source
        text.  This can be used for inline PageTemplates."""

    def PageTemplateFile(filename):
        """Create a Grok PageTemplate object from a file specified by
        ``filename``.  It will be treated like an inline template
        created with ``PageTemplate``."""

    def Fields(*args, **kw):
        """Return a list of formlib fields based on interfaces and/or schema
        fields."""

    def AutoFields(context):
        """Return a list of fields for context autogenerated by grok.
        """

    def action(label, actions=None, **options):
        """grok-specific action decorator.
        """


class IGrokView(IBrowserPage):
    """Grok views all provide this interface."""

    context = interface.Attribute('context', "Object that the view presents.")

    request = interface.Attribute('request', "Request that the view was looked"
                                  "up with.")

    response = interface.Attribute('response', "Response object that is "
                                   "associated with the current request.")

    static = interface.Attribute('static', "Directory resource containing "
                                 "the static files of the view's package.")

    def redirect(url):
       """Redirect to given URL"""

    def url(obj=None, name=None):
        """Construct URL.

        If no arguments given, construct URL to view itself.

        If only obj argument is given, construct URL to obj.

        If only name is given as the first argument, construct URL
        to context/name.

        If both object and name arguments are supplied, construct
        URL to obj/name.
        """

    def update(**kw):
        """This method is meant to be implemented by grok.View
        subclasses.  It will be called *before* the view's associated
        template is rendered and can be used to pre-compute values
        for the template.

        update() can take arbitrary keyword parameters which will be
        filled in from the request (in that case they *must* be
        present in the request)."""

    def render(**kw):
        """A view can either be rendered by an associated template, or
        it can implement this method to render itself from Python.
        This is useful if the view's output isn't XML/HTML but
        something computed in Python (plain text, PDF, etc.)

        render() can take arbitrary keyword parameters which will be
        filled in from the request (in that case they *must* be
        present in the request)."""

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
