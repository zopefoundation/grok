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
from zope import component, interface
from zope.traversing.browser.interfaces import IAbsoluteURL
from zope.traversing.browser.absoluteurl import _safe as SAFE_URL_CHARACTERS

from zope.security.checker import NamesChecker, defineChecker
from zope.security.interfaces import IPermission

from martian.error import GrokError, GrokImportError
from martian.util import class_annotation, methods_from_class, scan_for_classes

def check_adapts(class_):
    if component.adaptedBy(class_) is None:
        raise GrokError("%r must specify which contexts it adapts "
                        "(use grok.adapts to specify)."
                        % class_, class_)

def make_checker(factory, view_factory, permission, method_names=None):
    """Make a checker for a view_factory associated with factory.

    These could be one and the same for normal views, or different
    in case we make method-based views such as for JSON and XMLRPC.
    """
    if method_names is None:
        method_names = ['__call__']
    if permission is not None:
        check_permission(factory, permission)
    if permission is None or permission == 'zope.Public':
        checker = NamesChecker(method_names)
    else:
        checker = NamesChecker(method_names, permission)
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

def _sort_key(component):
    # If components have a grok.order directive, sort by that.
    explicit_order, implicit_order = class_annotation(
        component, 'grok.order', (0,0))
    return (explicit_order,
            component.__module__,
            implicit_order,
            component.__class__.__name__)

def sort_components(components):
    return sorted(components, key=_sort_key)

AMBIGUOUS_COMPONENT = object()
def check_module_component(factory, component,
                           component_name, component_directive):
    """Raise error if module-level component cannot be determined.

    If the module-level component is None, it's never been specified;
    raise error telling developer to specify.

    if the module-level component is AMBIGUOUS_COMPONENT, raise
    an error telling developer to specify which one to use.
    """
    if component is None:
        raise GrokError("No module-level %s for %r, please use "
                        "%s." % (component_name, factory, component_directive),
                        factory)
    elif component is AMBIGUOUS_COMPONENT:
        raise GrokError("Multiple possible %ss for %r, please use "
                        "%s." % (component_name, factory, component_directive),
                        factory)

def determine_module_component(module_info, annotation, classes):
    """Determine module-level component.

    The module-level component can be set explicitly using the
    annotation (such as grok.context).

    If there is no annotation, the module-level component is determined
    by scanning for subclasses of any in the list of classes.

    If there is no module-level component, the module-level component is
    None.

    If there is one module-level component, it is returned.

    If there are more than one module-level component, AMBIGUOUS_COMPONENT
    is returned.
    """
    components = scan_for_classes(module_info.getModule(), classes)
    if len(components) == 0:
        component = None
    elif len(components) == 1:
        component = components[0]
    else:
        component= AMBIGUOUS_COMPONENT

    module_component = module_info.getAnnotation(annotation, None)
    if module_component:
        component = module_component
    return component


def determine_class_component(module_info, class_,
                              component_name, component_directive):
    """Determine component for a class.

    Determine a component for a class. If no class-specific component exists,
    try falling back on module-level component.
    """
    module_component = module_info.getAnnotation(component_directive, None)
    component = class_annotation(class_, component_directive, module_component)
    check_module_component(class_, component,
                           component_name, component_directive)
    return component

def check_provides_one(obj):
    provides = list(interface.providedBy(obj))
    if len(provides) < 1:
        raise GrokError("%r must provide at least one interface "
                        "(use zope.interface.classProvides to specify)."
                        % obj, obj)
    if len(provides) > 1:
        raise GrokError("%r provides more than one interface "
                        "(use grok.provides to specify which one to use)."
                        % obj, obj)
