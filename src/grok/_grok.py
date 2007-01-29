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
import os.path
import sys
import time

from zope import component, interface
from zope.component.interfaces import IDefaultViewName
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.app.component.site import LocalSiteManager

import grok
from grok import util, scan, components, grokker, meta
from grok.error import GrokError, GrokImportError
from grok.directive import frame_is_module


_bootstrapped = False
def bootstrap():
    component.provideAdapter(components.ModelTraverser)
    component.provideAdapter(components.ContainerTraverser)

    # Register the name 'index' as the default view name.
    component.provideAdapter('index',
                             adapts=(grok.Model, IBrowserRequest),
                             provides=IDefaultViewName)
    component.provideAdapter('index',
                             adapts=(grok.Container, IBrowserRequest),
                             provides=IDefaultViewName)
    # Register a subscriber for when grok.Sites are added to make them
    # into Zope 3 sites.
    component.provideHandler(
        addSiteHandler, adapts=(grok.Site, grok.IObjectAddedEvent))

    # Now grok the grokkers.
    grokker.grokkerRegistry.grok(scan.module_info_from_module(meta))

def addSiteHandler(site, event):
    sitemanager = LocalSiteManager(site)
    # LocalSiteManager creates the 'default' folder in its __init__.
    # It's not needed anymore in new versions of Zope 3, therefore we
    # remove it
    del sitemanager['default']
    site.setSiteManager(sitemanager)

# Add a cleanup hook so that grok will bootstrap itself again whenever
# the Component Architecture is torn down.
def resetBootstrap():
    global _bootstrapped
    # we need to make sure that the grokker registry is clean again
    grokker.grokkerRegistry.clear()
    _bootstrapped = False
from zope.testing.cleanup import addCleanUp
addCleanUp(resetBootstrap)

_grokked_modules = []  # This is deliberately a list as grokking order matters.
def do_grok(dotted_name):
    global _bootstrapped
    if not _bootstrapped:
        bootstrap()
        _bootstrapped = True

    module_info = scan.module_info_from_dotted_name(dotted_name)
    grok_tree(module_info)
    _grokked_modules.append(dotted_name)

_grokked_tree = set()  # all modules that were ever looked at for grokking
_grokked_paths = set() # paths to watch for reload
def grok_tree(module_info):
    grokker.grokkerRegistry.grok(module_info)
    _grokked_tree.add(module_info.dotted_name)

    # Remember the file path to look at for reload; also remember the
    # directory it's in, in case a new module is placed next to it or
    # it's removed.
    _grokked_paths.add(module_info.path)
    _grokked_paths.add(os.path.dirname(module_info.path))

    for sub_module_info in module_info.getSubModuleInfos():
        grok_tree(sub_module_info)

_last_reload = time.time()
def reload_grokked_modules():
    # Throw away the registrations and reinitialize the grokker
    # registry (including registering grok's default grokkers again).
    grokker.grokkerRegistry.ungrok()
    grokker.grokkerRegistry.clear()
    grokker.grokkerRegistry.grok(scan.module_info_from_module(meta))

    # Throw away the modules so they will have to be reimported.
    for dotted_name in _grokked_tree:
        del sys.modules[dotted_name]
    _grokked_tree.clear()
    _grokked_paths.clear()
    # TODO what if the new modules contain errors?

    # re-grok all the modules that were grokked before (not the tree,
    # just the ones that were actually passed to do_grok, e.g. the
    # packages)
    grok_again = _grokked_modules[:]
    _grokked_modules[:] = []
    for dotted_name in grok_again:
        do_grok(dotted_name)

    global _last_reload
    _last_reload = time.time()

def check_reload():
    """Determines whether reload is necessary"""
    for path in _grokked_paths:
        if not os.path.exists(path):
            # The file was probably deleted, so reload.
            return True
        if os.stat(path).st_mtime > _last_reload:
            return True

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
