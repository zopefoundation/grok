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
"""Base classes for Grok application components.

When an application developer builds a Grok-based application, the
classes they define each typically inherit from one of the base classes
provided here.

"""
import persistent
import simplejson

import zope.location
from zope import component
from zope import interface
from zope.securitypolicy.role import Role as securitypolicy_Role
from zope.publisher.browser import BrowserPage
from zope.publisher.interfaces import NotFound
from zope.publisher.interfaces.browser import IBrowserPublisher
from zope.publisher.interfaces.http import IHTTPRequest
from zope.publisher.publish import mapply
from zope.annotation.interfaces import IAttributeAnnotatable

from zope.app.publisher.browser import getDefaultViewName
from zope.app.container.btree import BTreeContainer
from zope.app.container.contained import Contained
from zope.app.container.interfaces import IReadContainer, IObjectAddedEvent
from zope.app.container.interfaces import IOrderedContainer
from zope.app.container.contained import notifyContainerModified
from persistent.list import PersistentList
from zope.app.component.site import SiteManagerContainer
from zope.app.component.site import LocalSiteManager

import grok
import z3c.flashmessage.interfaces
import martian.util

import grokcore.view
from grok import interfaces, util


class Model(Contained, persistent.Persistent):
    # XXX Inheritance order is important here. If we reverse this,
    # then containers can't be models anymore because no unambigous MRO
    # can be established.
    """The base class for models in Grok applications.

    When an application class inherits from `grok.Model`, it gains the
    ability to persist itself in the Zope object database along with all
    of its attributes, and to remember the container in which it has
    been placed (its "parent") so that its URL can be computed.  It also
    inherits the `IContext` marker interface, which can make it the
    default context for views in its module; the rule is that if a
    module contains `grok.View` classes or other adapters that do not
    define a `grok.context()`, but the module also defines exactly one
    class that provides the `IContext` interface, then that class will
    automatically be made the `grok.context()` of each of the views.

    """
    interface.implements(IAttributeAnnotatable, interfaces.IContext)


class Container(BTreeContainer):
    """The base class for containers in Grok applications.

    When an application class inherits from `grok.Container`, it not
    only has the features of a `grok.Model` (persistance, location, and
    the ability to serve as a default context for other classes), but it
    also behaves like a persistent dictionary.  To store items inside a
    container, simply use the standard Python getitem/setitem protocol::

        mycontainer['counter'] = 72
        mycontainer['address'] = mymodel
        mycontainer['subfolder'] = another_container

    By default, the URL of each item inside a container is the
    container's own URL followed by a slash and the key (like 'counter'
    or 'address') under which that item has been stored.

    """
    interface.implements(IAttributeAnnotatable, interfaces.IContainer)


class OrderedContainer(Container):
    """A Grok container that remembers the order of its items.

    This straightforward extension of the basic `grok.Container`
    remembers the order in which items have been inserted, so that
    `keys()`, `values()`, `items()`, and iteration across the container
    can all return the items in the order they were inserted.  The only
    way of changing the order is to call the `updateOrder()` method.

    """
    interface.implements(IOrderedContainer)

    def __init__(self):
        super(OrderedContainer, self).__init__()
        self._order = PersistentList()

    def keys(self):
        # Return a copy of the list to prevent accidental modifications.
        return self._order[:]

    def __iter__(self):
        return iter(self.keys())

    def values(self):
        return (self[key] for key in self._order)

    def items(self):
        return ((key, self[key]) for key in self._order)

    def __setitem__(self, key, object):
        foo = self.has_key(key)
        # Then do whatever containers normally do.
        super(OrderedContainer, self).__setitem__(key, object)
        if not foo:
            self._order.append(key)

    def __delitem__(self, key):
        # First do whatever containers normally do.
        super(OrderedContainer, self).__delitem__(key)
        self._order.remove(key)

    def updateOrder(self, order):
        """Impose a new order on the items in this container.

        Items in this container are, by default, returned in the order
        in which they were inserted.  To change the order, provide an
        argument to this method that is a sequence containing every key
        already in the container, but in a new order.

        """
        if set(order) != set(self._order):
            raise ValueError("Incompatible key set.")

        self._order = PersistentList()
        self._order.extend(order)
        notifyContainerModified(self)


class Site(SiteManagerContainer):
    """Mixin for creating sites in Grok applications.

    When an application `grok.Model` or `grok.Container` also inherits
    from `grok.Site`, then it can additionally support the registration
    of local Component Architecture entities like `grok.LocalUtility`
    and `grok.Indexes` objects; see those classes for more information.

    """


@component.adapter(Site, IObjectAddedEvent)
def addSiteHandler(site, event):
    """Add a local site manager to a Grok site object upon its creation.

    Grok registers this function so that it gets called each time a
    `grok.Site` instance is added to a container.  It creates a local
    site manager and installs it on the newly created site.

    """
    sitemanager = LocalSiteManager(site)
    # LocalSiteManager creates the 'default' folder in its __init__.
    # It's not needed anymore in new versions of Zope 3, therefore we
    # remove it
    del sitemanager['default']
    site.setSiteManager(sitemanager)


class Application(Site):
    """Mixin for creating Grok application objects.

    When a `grok.Container` (or a `grok.Model`, though most developers
    use containers) also inherits from `grok.Application`, it not only
    gains the component registration abilities of a `grok.Site`, but
    will also be listed in the Grok admin control panel as one of the
    applications that the admin can install directly at the root of
    their Zope database.

    """
    interface.implements(interfaces.IApplication)


class LocalUtility(Model):
    """The base class for local utilities in Grok applications.

    Although application developers can create local utilies without
    actually subclassing `grok.LocalUtility`, they gain three benefits
    from doing so.  First, their code is more readable because their
    classes "look like" local utilities to casual readers.  Second,
    their utility will know how to persist itself to the Zope database,
    which means that they can set its object attributes and know that
    the values are getting automatically saved.  Third, they can omit
    the `grok.provides()` directive naming the interface that the
    utility provides, if their class only `grok.implements()` a single
    interface (unless the interface is one that the `grok.LocalUtility`
    already implements, in which case Grok cannot tell them apart, and
    `grok.provides()` must be used explicitly anyway).

    """


class Annotation(persistent.Persistent):
    """The base class for annotation classes in Grok applications."""


class View(grokcore.view.View):
    """The base class for views in Grok applications.

    Each class that inherits from `grok.View` is designed to "render" a
    category of content objects by reducing them to a document (often an
    HTML document).  Every view has a name, and is invoked when users
    visit the URL of an eligible context object followed by the name of
    the view itself::

        http://example.com/app/folder/object/viewname

    If ``viewname`` might conflict with actual content inside of the
    context (because the context already contains an attribute or item
    named ``viewname``), then the URL can be explicit that it is asking
    for the view by preceding its name with ``@@``::

        http://example.com/app/folder/object/@@viewname

    Instead of returning a full document, views are sometimes used to
    provide only a snippet of information for inclusion in some larger
    document; the view can then be called from inside of another view's
    page template::

        <li tal:content="context/@@viewname">snippet goes here</li>

    A view class can specify the category of objects that it can render
    by calling the `grok.context()` with either a class or an interface.
    Otherwise, Grok will attempt to determine the context automatically
    by searching the view's module for exactly one `grok.Model` or
    `grok.Container` class (or some other class providing the interface
    `IContext`) and using that class, if found.

    Grok normally creates a view's name (the name used in URLs) by
    downcasing the name of the view class itself.  The developer can
    override this by supplying the `grok.name()` directive instead.

    The view name ``index`` is special (this works whether the view
    class itself is named ``Index``, or whether ``grok.name('index')``
    is used instead).  A view named ``index`` is used to render an
    object when the user visits its URL without appending a view name.

    Each view should either provide a `render()` method that simply
    returns a document, or should have an accompanying page template.
    Grok will automatically find the correct page template if (a) it is
    in a directory next to the view's module, whose name is the module
    name followed by `_templates`; (b) its filename is the downcased
    name of the view class; and (c) it has an extension (such as ``.pt``
    for Zope Page Templates) that Grok recognizes.  Otherwise, the
    developer can name a page template file explicitly with the
    `grok.template()` directive.  Before the template is rendered, Grok
    will call the `update()` method on the view, if one is supplied,
    which can pre-compute values that the template will need to display.

    Both `render()` methods and `update()` methods will find the context
    for which the view is being rendered under ``self.context``.

    """
    interface.implements(interfaces.IGrokView)

    def application_url(self, name=None):
        """Return the URL of the nearest enclosing `grok.Application`."""
        obj = self.context
        while obj is not None:
            if isinstance(obj, Application):
                return self.url(obj, name)
            obj = obj.__parent__
        raise ValueError("No application found.")

    def flash(self, message, type='message'):
        """Send a short message to the user."""
        # XXX this has no tests or documentation, anywhere
        source = component.getUtility(
            z3c.flashmessage.interfaces.IMessageSource, name='session')
        source.send(message, type)


class Form(grokcore.formlib.Form, View):
    interface.implements(interfaces.IGrokForm)


class AddForm(grokcore.formlib.AddForm, View):
    interface.implements(interfaces.IGrokForm)


class DisplayForm(grokcore.formlib.DisplayForm, View):
    interface.implements(interfaces.IGrokForm)


class EditForm(grokcore.formlib.EditForm, View):
    interface.implements(interfaces.IGrokForm)


class XMLRPC(object):
    pass

class REST(zope.location.Location):
    interface.implements(interfaces.IREST)

    def __init__(self, context, request):
        self.context = self.__parent__ = context
        self.request = request
        self.body = request.bodyStream.getCacheStream().read()

    @property
    def response(self):
        return self.request.response

class JSON(BrowserPage):
    interface.implements(interfaces.IGrokSecurityView)
    
    def __call__(self):
        view_name = self.__view_name__
        method = getattr(self, view_name)
        method_result = mapply(method, (), self.request)
        return simplejson.dumps(method_result)


class Traverser(object):
    interface.implements(IBrowserPublisher)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def browserDefault(self, request):
        # if we have a RESTful request, we will handle
        # GET, POST and HEAD differently (PUT and DELETE are handled already
        # but not on the BrowserRequest layer but the HTTPRequest layer)
        if interfaces.IRESTLayer.providedBy(request):
            rest_view = component.getMultiAdapter(
                (self.context, self.request), name=request.method)
            return rest_view, ()
        view_name = getDefaultViewName(self.context, request)
        view_uri = "@@%s" % view_name
        return self.context, (view_uri,)

    def publishTraverse(self, request, name):
        subob = self.traverse(name)
        if subob is not None:
            return util.safely_locate_maybe(subob, self.context, name)

        traversable_dict = grok.traversable.bind().get(self.context)
        if traversable_dict:
            if name in traversable_dict:
                subob = getattr(self.context, traversable_dict[name])
                if callable(subob):
                    subob = subob()
                return util.safely_locate_maybe(subob, self.context, name)

        # XXX Special logic here to deal with containers.  It would be
        # good if we wouldn't have to do this here. One solution is to
        # rip this out and make you subclass ContainerTraverser if you
        # wanted to override the traversal behaviour of containers.
        if IReadContainer.providedBy(self.context):
            item = self.context.get(name)
            if item is not None:
                return item

        view = component.queryMultiAdapter((self.context, request), name=name)
        if view is not None:
            return view

        raise NotFound(self.context, name, request)

    def traverse(self, name):
        # this will be overridden by subclasses
        pass


class ContextTraverser(Traverser):
    component.adapts(interfaces.IContext, IHTTPRequest)

    def traverse(self, name):
        traverse = getattr(self.context, 'traverse', None)
        if traverse:
            return traverse(name)


class ContainerTraverser(Traverser):
    component.adapts(interfaces.IContainer, IHTTPRequest)

    def traverse(self, name):
        traverse = getattr(self.context, 'traverse', None)
        if traverse:
            result = traverse(name)
            if result is not None:
                return result
        # try to get the item from the container
        return self.context.get(name)


class IndexesClass(object):
    def __init__(self, name, bases=(), attrs=None):
        if attrs is None:
            return
        indexes = {}
        for name, value in attrs.items():
            # Ignore everything that's not an index definition object
            # except for values set by directives
            if '.' in name:
                setattr(self, name, value)
                continue
            if not interfaces.IIndexDefinition.providedBy(value):
                continue
            indexes[name] = value
        self.__grok_indexes__ = indexes
        # __grok_module__ is needed to make defined_locally() return True for
        # inline templates
        self.__grok_module__ = martian.util.caller_module()

Indexes = IndexesClass('Indexes')


class Role(securitypolicy_Role):
    pass


