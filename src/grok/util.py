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
"""Grok utility functions.
"""

import urllib

import zope.location.location
from zope import component
from zope.traversing.browser.interfaces import IAbsoluteURL
from zope.traversing.browser.absoluteurl import _safe as SAFE_URL_CHARACTERS

from zope.security.checker import NamesChecker, defineChecker
from zope.security.interfaces import IPermission

from martian.error import GrokError, GrokImportError
from martian.util import class_annotation, methods_from_class

def check_adapts(class_):
    if component.adaptedBy(class_) is None:
        raise GrokError("%r must specify which contexts it adapts "
                        "(use grok.adapts to specify)."
                        % class_, class_)

def make_checker(factory, view_factory, permission):
    """Make a checker for a view_factory associated with factory.

    These could be one and the same for normal views, or different
    in case we make method-based views such as for JSON and XMLRPC.
    """
    if permission is not None:
        check_permission(factory, permission)
    if permission is None or permission == 'zope.Public':
        checker = NamesChecker(['__call__'])
    else:
        checker = NamesChecker(['__call__'], permission)
    defineChecker(view_factory, checker)

def check_permission(factory, permission):
    """Check whether a permission is defined.

    If not, raise error for factory.
    """
    if component.queryUtility(IPermission,
                              name=permission) is None:
       raise GrokError('Undefined permission %r in %r. Use '
                       'grok.Permission first.'
                       % (permission, factory), factory)

def get_default_permission(factory):
    """Determine the default permission for a view.
    
    There can be only 0 or 1 default permission.
    """
    permissions = class_annotation(factory, 'grok.require', [])
    if not permissions:
        return None
    if len(permissions) > 1:
        raise GrokError('grok.require was called multiple times in '
                        '%r. It may only be set once for a class.'
                        % factory, factory)

    result = permissions[0]
    return result

def url(request, obj, name=None):
    """Given a request and an object, give the URL.

    Optionally pass a third argument name which gets added to the URL.
    """    
    url = component.getMultiAdapter((obj, request), IAbsoluteURL)()
    if name is None:
        return url
    return url + '/' + urllib.quote(name.encode('utf-8'),
                                    SAFE_URL_CHARACTERS)

def safely_locate_maybe(obj, parent, name):
    """Set an object's __parent__ (and __name__) if the object's
    __parent__ attribute doesn't exist yet or is None.

    If the object provides ILocation, __parent__ and __name__ will be
    set directly.  A location proxy will be returned otherwise.
    """
    if getattr(obj, '__parent__', None) is not None:
        return obj
    # This either sets __parent__ or wraps 'obj' in a LocationProxy
    return zope.location.location.located(obj, parent, name)

def determine_class_directive(directive_name, factory, module_info,
                              default=None):
    directive = class_annotation(factory, directive_name, None)
    if directive is None:
        directive = module_info.getAnnotation(directive_name, None)
    if directive is not None:
        return directive
    return default

def public_methods_from_class(factory):
    return [m for m in methods_from_class(factory) if \
            not m.__name__.startswith('_')]
