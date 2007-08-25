##############################################################################
#
# Copyright (c) 2007 Zope Corporation and Contributors.
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
"""Grokkers for adapters, utilities, subscribers, etc.
"""
import martian
import zope.component.interface
from martian import util
from martian.error import GrokError
from grokcore.component import Adapter, MultiAdapter, GlobalUtility


def check_adapts(class_):
    if zope.component.adaptedBy(class_) is None:
        raise GrokError("%r must specify which contexts it adapts "
                        "(use grok.adapts to specify)."
                        % class_, class_)


class AdapterGrokker(martian.ClassGrokker):
    component_class = Adapter

    def grok(self, name, factory, module_info, context=None, **kw):
        adapter_context = util.determine_class_context(factory, context)
        provides = util.class_annotation(factory, 'grok.provides', None)
        if provides is None:
            util.check_implements_one(factory)
        name = util.class_annotation(factory, 'grok.name', '')
        zope.component.provideAdapter(factory, adapts=(adapter_context,),
                                      provides=provides,
                                      name=name)
        return True


class MultiAdapterGrokker(martian.ClassGrokker):
    component_class = MultiAdapter

    def grok(self, name, factory, module_info, **kw):
        provides = util.class_annotation(factory, 'grok.provides', None)
        if provides is None:
            util.check_implements_one(factory)
        check_adapts(factory)
        name = util.class_annotation(factory, 'grok.name', '')
        zope.component.provideAdapter(factory, provides=provides, name=name)
        return True


class GlobalUtilityGrokker(martian.ClassGrokker):
    component_class = GlobalUtility

    def grok(self, name, factory, module_info, **kw):
        provides = util.class_annotation(factory, 'grok.provides', None)
        if provides is None:
            util.check_implements_one(factory)
        name = util.class_annotation(factory, 'grok.name', '')
        zope.component.provideUtility(factory(), provides=provides, name=name)
        return True


class SubscriberGrokker(martian.GlobalGrokker):

    def grok(self, name, module, module_info, **kw):
        subscribers = module_info.getAnnotation('grok.subscribers', [])

        for factory, subscribed in subscribers:
            zope.component.provideHandler(factory, adapts=subscribed)
            for iface in subscribed:
                zope.component.interface.provideInterface('', iface)
        return True


class AdapterDecoratorGrokker(martian.GlobalGrokker):

    def grok(self, name, module, module_info, context=None, **kw):
        implementers = module_info.getAnnotation('implementers', [])
        for function in implementers:
            interfaces = getattr(function, '__component_adapts__', None)
            if interfaces is None:
                # There's no explicit interfaces defined, so we assume the
                # module context to be the thing adapted.
                util.check_context(module_info.getModule(), context)
                interfaces = (context, )
            zope.component.provideAdapter(
                function, adapts=interfaces, provides=function.__implemented__)
        return True
