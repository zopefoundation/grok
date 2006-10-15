##############################################################################
#
# Copyright (c) 2006 Zope Corporation and Contributors.
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
"""Grok
"""
import types
import sys
import re
from zope.dottedname.resolve import resolve
from zope import component
from zope import interface
from zope.interface.interfaces import IInterface
from zope.publisher.browser import BrowserPage
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.pagetemplate import pagetemplate
from zope.app.pagetemplate.engine import TrustedAppPT

class Model(object):
    pass

class Adapter(object):

    def __init__(self, context):
        self.context = context

class View(BrowserPage):

    def __call__(self):
        template = getattr(self, 'template', None)
        if not template:
            return self.render()

        namespace = template.pt_getContext()
        namespace['request'] = self.request
        namespace['view'] = self
        namespace['context'] = self.context
        return template.pt_render(namespace)

class PageTemplate(TrustedAppPT, pagetemplate.PageTemplate):
    expand = 0

    def __init__(self, template):
        super(PageTemplate, self).__init__()
        if not_unicode_or_ascii(template):
            raise GrokError("Invalid page template. Page templates must be "
                            "unicode or ASCII.")
        self.write(template)

        # XXX unfortunately using caller_module means that
        # PageTemplate cannot be subclassed
        self.__grok_module__ = caller_module()

class GrokError(Exception):
    pass

AMBIGUOUS_CONTEXT = object()
def grok(dotted_name):
    # TODO for now we only grok modules
    module = resolve(dotted_name)

    context = None
    adapters = []
    views = []
    templates = TemplateRegistry()
    for name in dir(module):
        obj = getattr(module, name)

        if not defined_locally(obj, dotted_name):
            continue

        if check_subclass(obj, Model):
            if context is None:
                context = obj
            else:
                context = AMBIGUOUS_CONTEXT
        elif check_subclass(obj, Adapter):
            adapters.append(obj)
        elif check_subclass(obj, View):
            views.append(obj)
        elif isinstance(obj, PageTemplate):
            templates.register(name, obj)

    if getattr(module, '__grok_context__', None):
        context = module.__grok_context__

    for factory in adapters:
        adapter_context = determine_context(factory, context)
        name = getattr(factory, '__grok_name__', '')
        component.provideAdapter(factory, adapts=(adapter_context,), name=name)

    for factory in views:
        view_context = determine_context(factory, context)
        factory_name = factory.__name__.lower()

        # find inline templates
        template_name = getattr(factory, '__grok_template__', factory_name)
        template = templates.get(template_name)
        if template:
            templates.markAssociated(template_name)
            factory.template = template
        else:
            if not getattr(factory, 'render', None):
                raise GrokError("View %r has no associated template or "
                                "'render' method." % factory)

        view_name = getattr(factory, '__grok_name__', factory_name)
        component.provideAdapter(factory,
                                 adapts=(view_context, IDefaultBrowserLayer),
                                 provides=interface.Interface,
                                 name=view_name)

    for name, unassociated in templates.listUnassociatedTemplates():
        source = '<%s template in %s>' % (name, dotted_name)
        check_context(source, context)

        class TemplateView(View):
            template = unassociated

        templates.markAssociated(name)

        component.provideAdapter(TemplateView,
                                 adapts=(context, IDefaultBrowserLayer),
                                 provides=interface.Interface,
                                 name=name)

class TemplateRegistry(object):

    def __init__(self):
        self._reg = {}

    def register(self, name, template):
        self._reg[name] = dict(template=template, associated=False)

    def markAssociated(self, name):
        self._reg[name]['associated'] = True

    def get(self, name):
        entry = self._reg.get(name)
        if entry is None:
            return None
        return entry['template']

    def listUnassociatedTemplates(self):
        for name, entry in self._reg.iteritems():
            if not entry['associated']:
                yield name, entry['template']

def defined_locally(obj, dotted_name):
    obj_module = getattr(obj, '__grok_module__', None)
    if obj_module is None:
        obj_module = getattr(obj, '__module__', None)
    return obj_module == dotted_name

def isclass(obj):
    """We cannot use ``inspect.isclass`` because it will return True for interfaces"""
    return type(obj) in (types.ClassType, type)

def check_subclass(obj, class_):
    if not isclass(obj):
        return False
    return issubclass(obj, class_)

def check_context(source, context):
    if context is None:
        raise GrokError("No module-level context for %s, please use "
                        "grok.context." % source)
    elif context is AMBIGUOUS_CONTEXT:
        raise GrokError("Multiple possible contexts for %s, please use "
                        "grok.context." % source)

def determine_context(factory, module_context):
    context = getattr(factory, '__grok_context__', module_context)
    check_context(repr(factory), context)
    return context

def caller_is_module():
    frame = sys._getframe(2)
    return frame.f_locals is frame.f_globals

def caller_is_class():
    frame = sys._getframe(2)
    return '__module__' in frame.f_locals

def caller_module():
    return sys._getframe(2).f_globals['__name__']

def set_local(name, value, error_message):
    frame = sys._getframe(2)
    name = '__grok_%s__' % name
    if name in frame.f_locals:
        raise GrokError(error_message)
    frame.f_locals[name] = value

def not_unicode_or_ascii(value):
    if isinstance(value, unicode):
        return False
    if not isinstance(value, str):
        return True
    return is_not_ascii(value)

is_not_ascii = re.compile(eval(r'u"[\u0080-\uffff]"')).search

def context(obj):
    if not (IInterface.providedBy(obj) or isclass(obj)):
        raise GrokError("You can only pass classes or interfaces to "
                        "grok.context.")
    if not (caller_is_module() or caller_is_class()):
        raise GrokError("grok.context can only be used on class or module level.")
    set_local('context', obj, "grok.context can only be called once per class "
              "or module.")

class ClassDirective(object):
    """
    Class-level directive that puts unicode/ASCII values into the
    class's locals as __grok_<name>__.
    """

    def __init__(self, name):
        self.name = name

    def __call__(self, val):
        if not_unicode_or_ascii(val):
            raise GrokError("You can only pass unicode or ASCII to "
                            "grok.%s." % self.name)
        if not caller_is_class():
            raise GrokError("grok.%s can only be used on class level."
                            % self.name)
        set_local(self.name, val, "grok.%s can only be called once per class."
                  % self.name)

name = ClassDirective('name')
template = ClassDirective('template')
