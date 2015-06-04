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
"""Grok utility functions.
"""
import zope.component.hooks
import zope.location.location

from zope import interface
from grokcore.view.util import url, ASIS
from grokcore.site.util import getApplication


def safely_locate_maybe(obj, parent, name):
    """Set an object's ``__parent__`` (and ``__name__``) if the object's
    ``__parent__`` attribute doesn't exist yet or is ``None``.

    If the object provides ``ILocation``, ``__parent__`` and
    ``__name__`` will be set directly.  A location proxy will be
    returned otherwise.
    """
    if getattr(obj, '__parent__', None) is not None:
        return obj
    # This either sets __parent__ or wraps 'obj' in a LocationProxy
    return zope.location.location.located(obj, parent, name)


def applySkin(request, skin, skin_type):
    """Change the presentation skin for this request.
    """
    # Remove all existing skin declarations (commonly the default skin).
    ifaces = [iface for iface in interface.directlyProvidedBy(request)
              if not skin_type.providedBy(iface)]
    # Add the new skin.
    ifaces.append(skin)
    interface.directlyProvides(request, *ifaces)


def application_url(request, obj, name=None, skin=ASIS, data={}):
    """Return the URL of the nearest enclosing :class:`grok.Application`.

    Raises :exc:`ValueError` if no application can be found.
    """
    return url(request, getApplication(), name=name, skin=skin, data=data)
