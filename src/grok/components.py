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
import types
import urllib

from zope import component
from zope import interface
from zope import schema
from zope.security.proxy import removeSecurityProxy
from zope.publisher.browser import BrowserPage
from zope.publisher.interfaces import NotFound
from zope.publisher.interfaces.browser import (IBrowserPublisher,
                                               IBrowserRequest)
from zope.pagetemplate import pagetemplate
from zope.formlib import form
from zope.formlib.namedtemplate import INamedTemplate
from zope.schema.interfaces import IField
from zope.traversing.browser.interfaces import IAbsoluteURL
from zope.traversing.browser.absoluteurl import AbsoluteURL
from zope.traversing.browser.absoluteurl import _safe as SAFE_URL_CHARACTERS

from zope.app.pagetemplate.engine import TrustedAppPT
from zope.app.publisher.browser import getDefaultViewName
from zope.app.publisher.browser import directoryresource
from zope.app.publisher.browser.pagetemplateresource import \
    PageTemplateResourceFactory
from zope.app.container.btree import BTreeContainer
from zope.app.container.contained import Contained

from grok import util, security, interfaces


class Model(Contained, persistent.Persistent):  
    # XXX Inheritance order is important here. If we reverse this, 
    # then containers can't be models anymore because no unambigous MRO 
    # can be established.
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
    interface.implements(interfaces.IGrokView)
    
    def __init__(self, context, request):
        # Jim would say: WAAAAAAAAAAAAH!
        self.context = removeSecurityProxy(context)
        self.request = removeSecurityProxy(request)
        self.directory_resource = component.queryAdapter(self.request,
                interface.Interface, name=self.module_info.package_dotted_name)

    def __call__(self):
        self.before()

        template = getattr(self, 'template', None)
        if not template:
            return self.render()

        namespace = template.pt_getContext()
        namespace['request'] = self.request
        namespace['view'] = self
        namespace['context'] = self.context
        # XXX need to check whether we really want to put None here if missing
        namespace['static'] = self.directory_resource
        return template.pt_render(namespace)

    def __getitem__(self, key):
        # XXX give nice error message if template is None
        return self.template.macros[key]

    def url(self, obj=None, name=None):
        # if the first argument is a string, that's the name. There should
        # be no second argument
        if isinstance(obj, basestring):
            if name is not None:
                raise TypeError(
                    'url() takes either obj argument, obj, string arguments, '
                    'or string argument')
            name = obj
            obj = None
            
        if name is None and obj is None:
            # create URL to view itself
            obj = self
        elif name is not None and obj is None:
            # create URL to view on context
            obj = self.context
        url = component.getMultiAdapter((obj, self.request), IAbsoluteURL)()
        if name is None:
            # URL to obj itself
            return url
        # URL to view on obj
        return url + '/' + urllib.quote(name.encode('utf-8'),
                                        SAFE_URL_CHARACTERS)
    
    def before(self):
        pass


class GrokViewAbsoluteURL(AbsoluteURL):
    def _getContextName(self, context):
        return getattr(context, '__view_name__', None)
    # XXX breadcrumbs method on AbsoluteURL breaks as it does not use
    # _getContextName to get to the name of the view. What does breadcrumbs do?
    

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

    def _annotateGrokInfo(self, name, location):
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

class Traverser(object):
    interface.implements(IBrowserPublisher)

    def __init__(self, context, request):
        # Jim would say: WAAAAAAAAAAAAH!
        self.context = removeSecurityProxy(context)
        self.request = removeSecurityProxy(request)

    def browserDefault(self, request):
        view_name = getDefaultViewName(self.context, request)
        view_uri = "@@%s" % view_name
        return self.context, (view_uri,)

    def publishTraverse(self, request, name):
        subob = self.traverse(name)
        if subob:
            return subob

        view = component.queryMultiAdapter((self.context, request), name=name)
        if view:
            return view

        raise NotFound(self.context, name, request)

    def traverse(self, name):
        # this will be overridden by subclasses
        pass


class ModelTraverser(Traverser):
    component.adapts(Model, IBrowserRequest)

    def traverse(self, name):
        traverser = util.class_annotation(self.context, 'grok.traverse', None)
        if traverser:
            return traverser(name)


class Form(View):
    def _init(self):
        fields = schema_fields(self.context)
        self.form_fields = form.Fields(*fields)

        self.template = component.getAdapter(self, INamedTemplate,
                                             name='default')
    def __call__(self):
        self.update()
        return self.render()

class EditForm(Form, form.EditForm):
    def __init__(self, context, request):
        super(EditForm, self).__init__(context, request)
        self._init()

    def default_handle_apply(self, action, data):
         form.EditForm.handle_edit_action.success_handler(self, action, data)

class DisplayForm(Form, form.DisplayForm):
    def __init__(self, context, request):
        super(DisplayForm, self).__init__(context, request)
        self._init()

def schema_fields(obj):
    fields = []
    fields_class = getattr(obj, 'fields', None)
    if fields_class is not None:
        if type(fields_class) == types.ClassType:
            for name in dir(fields_class):
                field = getattr(fields_class, name)
                if IField.providedBy(field):
                    if not getattr(field, '__name__', None):
                        field.__name__ = name
                    fields.append(field)
    return fields
