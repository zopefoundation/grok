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
"""Grok directives.

This module defines Grok directives: the markers that users place
inside of their classes (and sometimes in their modules, too) to
direct how Grok registers their components.  For example, the first
directive defined below is `site`, which people programming Grok
applications normally use like this::

    class MyIndex(grok.Indexes):
        grok.site(MySite)
        ...

If the set of directives in this module looks rather small, remember
that most of the directives available in Grok actually come from the
`grokcore` modules on which Grok depends, where they have been placed so
that other projects can use them without having to pull in all of Grok.

"""

import grok
import martian
import martian.util
from grokcore.view.directive import TaggedValueStoreOnce
from grokcore.rest.directive import restskin


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

    def validate(self, *values):
        for value in values:
            if martian.util.check_subclass(value, grok.Permission):
                continue
            if martian.util.not_unicode_or_ascii(value):
                raise grok.GrokImportError(
                    "You can only pass unicode values, ASCII values, or "
                    "subclasses of grok.Permission to the '%s' directive."
                    % self.name)

    def factory(self, *values):
        permission_ids = []
        for value in values:
            if martian.util.check_subclass(value, grok.Permission):
                permission_ids.append(grok.name.bind().get(value))
            else:
                permission_ids.append(value)
        return permission_ids
