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
"""Grok components"""

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
    """The base class for models in Grok applications.

    When an application class inherits from `grok.Model`, it not only
    gains the ability to persist itself in the Zope object database and
    to remember where in the database it lives (so that it can figure
    out its URL), but it is also marked with the `IContext` interface
    which tells Grok that the class is eligible to be auto-associated
    with `grok.View` classes or other adapters in its module which do
    not explicitly define a `grok.context()`.

    """
    # XXX Inheritance order is important here. If we reverse this,
    # then containers can't be models anymore because no unambigous MRO
    # can be established.
    interface.implements(IAttributeAnnotatable, interfaces.IContext)


class Container(BTreeContainer):
    """The base class for containers in Grok applications.

    A `grok.Container` subclass acts like a persistent dictionary, and
    knows both how to persist itself inside of a Zope database, and how
    to store other containers and models under its keys (using the
    standard Python getitem/setitem protocol).  By default, URLs which
    arrive at the container can continue on to objects inside of it by
    supplying a URL component that matches one of the container's keys.
    A `grok.Container` subclass is also marked with the `IContext`
    interface, which tells Grok that the class is eligible to be
    auto-associated with `grok.View` classes or other adapters in its
    module which do not explicitly define a `grok.context()`.

    """
    interface.implements(IAttributeAnnotatable, interfaces.IContainer)


class OrderedContainer(Container):
    """A Grok container that remembers the order of its items.

    This straightforward extension of the basic `grok.Container`
    remembers the order in which its keys pairs have been inserted, and
    allows their order to be modified later.  This means that keys and
    items returned by `keys()`, `values()`, and `items()`, as well as by
    iterating over the container, will appear in the same order as they
    were added to the container.  The only way of changing the item
    order in the container is through the method `updateOrder()`.

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
        in which they were inserted.  To impose a different ordering on
        the items instead, provide an `order` argument to this method
        that is a list containing every key already in the container,
        but in a new order.

        """
        if set(order) != set(self._order):
            raise ValueError("Incompatible key set.")

        self._order = PersistentList()
        self._order.extend(order)
        notifyContainerModified(self)


class Site(SiteManagerContainer):
    """The base class for sites in Grok applications.

    A `grok.Site` is a fancy container, with which Component
    Architecture entities like local utilities and indexes can be
    associated, that become active for all URLs that name either the
    site object itself or an object beneath the site.

    """


@component.adapter(Site, IObjectAddedEvent)
def addSiteHandler(site, event):
    """Add a local site manager to a Grok site object upon its creation.

    Grok registers this function so that it gets called each time a
    `grok.Site` instance is added to a container.  It creates a new
    local site manager and installs it on the site.

    """
    sitemanager = LocalSiteManager(site)
    # LocalSiteManager creates the 'default' folder in its __init__.
    # It's not needed anymore in new versions of Zope 3, therefore we
    # remove it
    del sitemanager['default']
    site.setSiteManager(sitemanager)


class Application(Site):
    """The base class for Grok applications.

    A `grok.Application` not only has all of the abilities of a Grok
    container (it can hold other objects) and a Grok site (it can be a
    registration point for local utilities), but application classes are
    specifically cataloged by Grok so that the Grok admin interface can
    list them in the menu of objects that users can instantiate directly
    inside of the root of their Zope database.

    """
    interface.implements(interfaces.IApplication)


class LocalUtility(Model):
    """The base class for local utilities in Grok applications.

    By inheriting from this `grok.LocalUtility` class when designing a
    local utility, Grok application authors accomplish three things.
    First, this class is knows how to persist itself to the database,
    which is important because local utilities must be stored in the
    Zope database alongside the `grok.Site` or `grok.Application` for
    which they are registered.  Second, Grok can deduce the interface
    that the utility is designed to provide if the utility simply
    `implements()` one interface (that is not already an interface
    provided by `grok.LocalUtility`, otherwise Grok cannot tell the
    difference); this saves the developer from having to supply an
    explicit `grok.provides()` directive.  Third, of course, their code
    will be easier to read if their local utilities inherit from
    something with "local utility" in its name.

    """


class Annotation(persistent.Persistent):
    """The base class for annotation classes in Grok applications."""


class View(grokcore.view.View):
    """The base class for views in Grok applications.

    Grok automatically registers each subclass of `grok.View` as able to
    render instances of its `grok.context()` for consumption by web
    browsers, when a specific `/name` is appended to the context's URL.
    The name can either be explicitly provided with `grok.name()`, or by
    default will be the downcased name of the class itself; Grok views
    with the name ``index`` are used by default if no `/name` is
    appended to the context's URL.

    """
    # XXX the above description needs either more detail, or less; I
    # will ask the Grok mailing list this morning - Brandon
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


