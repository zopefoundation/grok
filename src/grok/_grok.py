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
import os
import sys
import types

from zope import component
from zope import interface

from zope.component.interfaces import IDefaultViewName
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.app.component.site import LocalSiteManager

import martian
from martian import scan
from martian.error import GrokError, GrokImportError
from martian.util import frame_is_module, determine_module_context

import grok

from grok import components, meta
from grok import templatereg

_bootstrapped = False
def bootstrap():
    component.provideAdapter(components.ModelTraverser)
    component.provideAdapter(components.ContainerTraverser)

    # register the name 'index' as the default view name
    component.provideAdapter('index',
                             adapts=(grok.Model, IBrowserRequest),
                             provides=IDefaultViewName)
    component.provideAdapter('index',
                             adapts=(grok.Container, IBrowserRequest),
                             provides=IDefaultViewName)
    # register a subscriber for when grok.Sites are added to make them
    # into Zope 3 sites
    component.provideHandler(
        addSiteHandler, adapts=(grok.Site, grok.IObjectAddedEvent))

    # now grok the grokkers
    martian.grok_module(scan.module_info_from_module(meta), the_module_grokker)

def addSiteHandler(site, event):
    sitemanager = LocalSiteManager(site)
    # LocalSiteManager creates the 'default' folder in its __init__.
    # It's not needed anymore in new versions of Zope 3, therefore we
    # remove it
    del sitemanager['default']
    site.setSiteManager(sitemanager)

# add a cleanup hook so that grok will bootstrap itself again whenever
# the Component Architecture is torn down.
def resetBootstrap():
    global _bootstrapped
    # we need to make sure that the grokker registry is clean again
    the_module_grokker.clear()
    _bootstrapped = False
from zope.testing.cleanup import addCleanUp
addCleanUp(resetBootstrap)

def skip_tests(name):
    return name in ['tests', 'ftests']

def do_grok(dotted_name):
    global _bootstrapped
    if not _bootstrapped:
        bootstrap()
        _bootstrapped = True
    martian.grok_dotted_name(
        dotted_name, the_module_grokker, exclude_filter=skip_tests)

def grok_component(name, component,
                   context=None, module_info=None, templates=None):
    return the_multi_grokker.grok(name, component,
                                  context=context,
                                  module_info=module_info,
                                  templates=templates)

def prepare_grok(name, module, kw):
    module_info = scan.module_info_from_module(
        module, exclude_filter=skip_tests)

    # XXX hardcoded in here which base classes are possible contexts
    # this should be made extensible
    possible_contexts = martian.scan_for_classes(module, [grok.Model,
                                                          grok.Container])
    context = determine_module_context(module_info, possible_contexts)

    kw['context'] = context
    kw['module_info'] = module_info
    kw['templates'] = templatereg.TemplateRegistry()

def finalize_grok(name, module, kw):
    module_info = kw['module_info']
    templates = kw['templates']
    unassociated = list(templates.listUnassociated())
    if unassociated:
        raise GrokError("Found the following unassociated template(s) when "
                        "grokking %r: %s.  Define view classes inheriting "
                        "from grok.View to enable the template(s)."
                        % (module_info.dotted_name,
                           ', '.join(unassociated)), module_info)

the_multi_grokker = martian.MetaMultiGrokker()
the_module_grokker = martian.ModuleGrokker(the_multi_grokker,
                                           prepare=prepare_grok,
                                           finalize=finalize_grok)

# decorators
class SubscribeDecorator:

    def __init__(self, *args):
        self.subscribed = args

    def __call__(self, function):
        frame = sys._getframe(1)
        if not frame_is_module(frame):
            raise GrokImportError("@grok.subscribe can only be used on module "
                                  "level.")

        if not self.subscribed:
            raise GrokImportError("@grok.subscribe requires at least one "
                                  "argument.")

        subscribers = frame.f_locals.get('__grok_subscribers__', None)
        if subscribers is None:
            frame.f_locals['__grok_subscribers__'] = subscribers = []
        subscribers.append((function, self.subscribed))
        return function

from zope.component._declaration import adapter as _adapter
class adapter(_adapter):

    def __init__(self, *interfaces):
        # Override the z.c.adapter decorator to force sanity checking
        # and have better error reporting.
        if not interfaces:
            raise GrokImportError(
                "@grok.adapter requires at least one argument.")
        if type(interfaces[0]) is types.FunctionType:
            raise GrokImportError(
                "@grok.adapter requires at least one argument.")
        self.interfaces = interfaces

from zope.interface.declarations import implementer as _implementer
class implementer(_implementer):

    def __call__(self, ob):
        # XXX we do not have function grokkers (yet) so we put the annotation
        # on the module.
        frame = sys._getframe(1)
        implementers = frame.f_locals.get('__implementers__', None)
        if implementers is None:
            frame.f_locals['__implementers__'] = implementers = []
        implementers.append(ob)
        return _implementer.__call__(self, ob)
