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
"""Grok components
"""

import persistent
from zope import component
from zope import interface
from zope.proxy import removeAllProxies
from zope.publisher.browser import BrowserPage
from zope.pagetemplate import pagetemplate

from zope.app.pagetemplate.engine import TrustedAppPT
from zope.app.publisher.browser import directoryresource
from zope.app.publisher.browser.pagetemplateresource import \
    PageTemplateResourceFactory
from zope.app.container.btree import BTreeContainer

from grok import util, security

class Model(persistent.Persistent):
    pass


class Container(BTreeContainer):
    pass


class Adapter(object):

    def __init__(self, context):
        self.context = context


class Utility(object):
    pass

class MultiAdapter(object):
    pass

class View(BrowserPage):

    def __init__(self, context, request):
        self.context = removeAllProxies(context)
        self.request = removeAllProxies(request)

    def __call__(self):
        self.before()

        template = getattr(self, 'template', None)
        if not template:
            return self.render()

        namespace = template.pt_getContext()
        namespace['request'] = self.request
        # Jim would say: WAAAAAAAAAAAAH!
        namespace['view'] = self
        namespace['context'] = removeAllProxies(self.context)

        module_info = template.__grok_module_info__
        directory_resource = component.queryAdapter(self.request,
                interface.Interface, name=module_info.package_dotted_name)
        # XXX need to check whether we really want None here
        namespace['static'] = directory_resource
        return template.pt_render(namespace)

    def before(self):
        pass


class XMLRPC(object):
    pass



class PageTemplate(TrustedAppPT, pagetemplate.PageTemplate):
    expand = 0

    def __init__(self, template):
        super(PageTemplate, self).__init__()
        if util.not_unicode_or_ascii(template):
            raise ValueError("Invalid page template. Page templates must be "
                             "unicode or ASCII.")
        self.write(template)

        # __grok_module__ is needed to make defined_locally() return True for
        # inline templates
        # XXX unfortunately using caller_module means that
        # PageTemplate cannot be subclassed
        self.__grok_module__ = util.caller_module()

    def __repr__(self):
        return '<%s template in %s>' % (self.__grok_name__,
                                        self.__grok_location__)

    def _annotateGrokInfo(self, module_info, name, location):
        self.__grok_module_info__ = module_info
        self.__grok_name__ = name
        self.__grok_location__ = location


class DirectoryResource(directoryresource.DirectoryResource):
    # We subclass this, because we want to override the default factories for
    # the resources so that .pt and .html do not get created as page
    # templates

    resource_factories = {}
    for type, factory in (directoryresource.DirectoryResource.
                          resource_factories.items()):
        if factory is PageTemplateResourceFactory:
            continue
        resource_factories[type] = factory


class DirectoryResourceFactory(object):
    # We need this to allow hooking up our own GrokDirectoryResource
    # and to set the checker to None (until we have our own checker)

    def __init__(self, path, name):
        # XXX we're not sure about the checker=None here
        self.__dir = directoryresource.Directory(path, None, name)
        self.__name = name

    def __call__(self, request):
        resource = DirectoryResource(self.__dir, request)
        resource.__Security_checker__ = security.GrokChecker()
        resource.__name__ = self.__name
        return resource

