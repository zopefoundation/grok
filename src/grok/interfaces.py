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
    Adapter = interface.Attribute("Base class for adapters.")
    MultiAdapter = interface.Attribute("Base class for multi-adapters.")
    GlobalUtility = interface.Attribute("Base class for global utilities.")
    LocalUtility = interface.Attribute("Base class for local utilities.")
    View = interface.Attribute("Base class for browser views.")
    XMLRPC = interface.Attribute("Base class for XML-RPC methods.")
    Traverser = interface.Attribute("Base class for custom traversers.")
    EditForm = interface.Attribute("Base class for edit forms.")
    DisplayForm = interface.Attribute("Base class for display forms.")
    AddForm = interface.Attribute("Base class for add forms.")
    
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

    def template(template):
        """Declare the template name for a view.

        This directive can only be used on class level."""

    def templatedir(directory):
        """Declare a directory to be searched for templates.

        By default, grok will take the name of the module as the name
        of the directory.  This can be overridden using
        ``templatedir``."""

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

    def define_permission(permission):
        """Defines a new permission with the id ``permission``."""

    def require(permission):
        """Protect a view class or an XMLRPC method with ``permision``.

        ``permission`` already be define, e.g. using
        grok.define_permission.

        grok.require can be used as a class-level directive or as a
        method decorator."""

class IGrokDecorators(interface.Interface):

    def subscribe(*classes_or_interfaces):
        """Declare that a function subscribes to an event or a
        combination of objects and events."""

    def action():
        """XXX see zope.formlib.form.action"""

    traverse = interface.Attribute("Specify a method to be used for "
                                   "traversing URL paths.")

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

    def notify(event):
        """Send ``event`` to event subscribers."""

    def getSite():
        """Get the current site."""

    def PageTemplate(template):
        """Create a Grok PageTemplate object from ``template`` source
        text.  This can be used for inline PageTemplates."""

    def Fields(*args, **kw):
        """Return a list of formlib fields based on interfaces and/or schema
        fields."""

    def AutoFields(context):
        """Return a list of fields for context autogenerated by grok.
        """
        
    def action(label, actions=None, **options):
        """grok-specific action decorator.
        """

class IGrokView(interface.Interface):
    """Grok views all provide this interface.
    """
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
