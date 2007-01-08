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

from zope import component
from zope import interface

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
    grokker.grokkerRegistry.grok(scan.module_info_from_module(meta))

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
    grokker.grokkerRegistry.clear()
    _bootstrapped = False
from zope.testing.cleanup import addCleanUp
addCleanUp(resetBootstrap)


def do_grok(dotted_name):
    global _bootstrapped
    if not _bootstrapped:
        bootstrap()
        _bootstrapped = True

    module_info = scan.module_info_from_dotted_name(dotted_name)
    grok_tree(module_info)


def grok_tree(module_info):
    grokker.grokkerRegistry.grok(module_info)

    for sub_module_info in module_info.getSubModuleInfos():
        grok_tree(sub_module_info)

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
