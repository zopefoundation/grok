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
"""Grok directives.

This module defines Grok directives: the markers that users place inside
of their classes (and sometimes in their modules, too) to direct how
Grok registers their components.  For example, the first directive
defined below is `local_utility`, which people programming Grok
applications normally use like this::

    class MyUtility(grok.Utility):
        grok.local_utility()
        ...

If the set of directives in this module looks rather small, remember
that most of the directives available in Grok actually come from the
`grokcore` modules on which Grok depends, where they have been placed so
that other projects can use them without having to pull in all of Grok.

"""
import grok
from zope import interface
from zope.interface.interfaces import IInterface

import martian
from martian import util
from martian.error import GrokImportError
from grokcore.view.directive import TaggedValueStoreOnce

class local_utility(martian.Directive):
    """The `grok.local_utility()` directive.

    Place this directive inside of a `grok.Application` or `grok.Site`
    subclass, and provide the name of a utility you want activated
    inside of that site::

        class MySite(grok.Site):
            grok.local_utility(MyMammothUtility)
            ...

    This directive can be supplied several times within the same site.
    Thanks to the presence of this directive, any time an instance of
    your class is created in the Zope database it will have a copy of
    the given local utility installed along with it.

    This directive accepts several normal Component-registration keyword
    arguments, like `provides` and `name`, and uses them each time it
    registers your local utility.

    If you do not supply a `provides` keyword, then Grok attempts to
    guess a sensible default.  Its first choice is to use any
    interface(s) that you listed with the grok.provides() directive when
    defining your utility.  Otherwise, if your utility is a subclass of
    `grok.localUtility`, then Grok will use any interfaces that your
    utility supplies beyond those are supplied because of its
    inheritance from `grok.localUtility`.  Else, as a final fallback, it
    checks to see whether the class you are registering supplies one,
    and only one, interface; if so, then it can register the utility
    unambiguously as providing that one interface.

    """
    scope = martian.CLASS
    store = martian.DICT

    def factory(self, factory, provides=None, name=u'',
                setup=None, public=False, name_in_container=None):
        if provides is not None and not IInterface.providedBy(provides):
            raise GrokImportError("You can only pass an interface to the "
                                  "provides argument of %s." % self.name)

        if provides is None:
            provides = grok.provides.bind().get(factory)

        if provides is None:
            if util.check_subclass(factory, grok.LocalUtility):
                baseInterfaces = interface.implementedBy(grok.LocalUtility)
                utilityInterfaces = interface.implementedBy(factory)
                provides = list(utilityInterfaces - baseInterfaces)

                if len(provides) == 0 and len(list(utilityInterfaces)) > 0:
                    raise GrokImportError(
                        "Cannot determine which interface to use "
                        "for utility registration of %r. "
                        "It implements an interface that is a specialization "
                        "of an interface implemented by grok.LocalUtility. "
                        "Specify the interface by either using grok.provides "
                        "on the utility or passing 'provides' to "
                        "grok.local_utility." % factory, factory)
            else:
                provides = list(interface.implementedBy(factory))

            util.check_implements_one_from_list(provides, factory)
            provides = provides[0]

        if (provides, name) in self.frame.f_locals.get(self.dotted_name(), {}):
            raise GrokImportError(
                "Conflicting local utility registration %r. "
                "Local utilities are registered multiple "
                "times for interface %r and name %r." %
                (factory, provides, name), factory)

        info = LocalUtilityInfo(factory, provides, name, setup, public,
                                name_in_container)
        return (provides, name), info


class LocalUtilityInfo(object):
    """The information about how to register a local utility.

    An instance of this class is created for each `grok.local_utility()`
    in a Grok application's code, to remember how the user wants their
    local utility registered.  Later, whenever the application creates
    new instances of the site or application for which the local utility
    directive was supplied, this block of information is used as the
    parameters to the creation of the local utility which is created
    along with the new site in the Zope database.

    """
    _order = 0

    def __init__(self, factory, provides, name=u'',
                 setup=None, public=False, name_in_container=None):
        self.factory = factory
        self.provides = provides
        self.name = name
        self.setup = setup
        self.public = public
        self.name_in_container = name_in_container

        self.order = LocalUtilityInfo._order
        LocalUtilityInfo._order += 1

    def __cmp__(self, other):
        # LocalUtilityInfos have an inherit sort order by which the
        # registrations take place.
        return cmp(self.order, other.order)


class site(martian.Directive):
    """The `grok.site()` directive.

    This directive is used when creating a `grok.Indexes` subclass, to
    indicate the Grok site object for which the indexes should be built.

    """
    scope = martian.CLASS
    store = martian.ONCE
    validate = martian.validateInterfaceOrClass

class permissions(martian.Directive):
    """The `grok.permissions()` directive.

    This directive is used inside of a `grok.Role` subclass to list the
    permissions which each member of the role should always possess.
    Note that permissions should be passed as strings, and that several
    permissions they can simply be supplied as multiple arguments; there
    is no need to place them inside of a tuple or list::

        class MyRole(grok.Role):
            grok.permissions('page.CreatePage', 'page.EditPage')
            ...

    """
    scope = martian.CLASS
    store = martian.ONCE
    default = []

    def factory(self, *args):
        return args

class traversable(martian.Directive):
    """The `grok.traversable()` directive.

    Each time this directive is used inside of a class, it designates an
    attribute of that class which URLs should be able to traverse.  For
    example, the declaration:

        class Mammoth(grok.Model):
            grok.traversable('thighbone')

    means that if the URL `/app/mymammoth` designates a Mammoth, then
    `/app/mymammoth/thighbone` will also be a valid URL (assuming that
    the Mammoth instance, at runtime, indeed has an attribute by that
    name)!  By default, the name that must be appended to the URL should
    simply be the same as the name of the attribute; but by providing a
    `name` keyword argument, the programmer can designate another name
    to appear in the URL instead of the raw attribute name.

    """
    scope = martian.CLASS
    store = martian.DICT

    def factory(self, attr, name=None):
        if name is None:
            name = attr
        return (name, attr)

class restskin(martian.Directive):
    """The `grok.restskin()` directive.

    This directive is placed inside of `grok.IRESTLayer` subclasses to
    indicate what their layer name will be within a REST URL.  Giving
    the skin ``grok.restskin('b')``, for example, will enable URLs that
    look something like `http://localhost/++rest++b/app`.

    """
    # We cannot do any better than to check for a class scope. Ideally we
    # would've checked whether the context is indeed an Interface class.
    scope = martian.CLASS
    store = TaggedValueStoreOnce()
    validate = martian.validateText

    def factory(self, value=None):
        return value
