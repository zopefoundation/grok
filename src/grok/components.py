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
import urllib

from zope import component
from zope import interface
from zope import schema
from zope import event
from zope.lifecycleevent import ObjectModifiedEvent
from zope.publisher.browser import BrowserPage
from zope.publisher.interfaces import NotFound
from zope.publisher.interfaces.browser import (IBrowserPublisher,
                                               IBrowserRequest)
from zope.pagetemplate import pagetemplate
from zope.formlib import form
from zope.formlib.namedtemplate import INamedTemplate
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
from zope.app.container.interfaces import IReadContainer
from zope.app.component.site import SiteManagerContainer

from grok import util, interfaces


class GrokkerBase(object):
    """A common base class for all grokkers.
    """

    priority = 0
    continue_scanning = False


class ClassGrokker(GrokkerBase):
    """Grokker for particular classes in a module.
    """
    # subclasses should have a component_class class variable

    def match(self, obj):
        return util.check_subclass(obj, self.component_class)

    def register(self, context, name, factory, module_info, templates):
        raise NotImplementedError


class InstanceGrokker(GrokkerBase):
    """Grokker for particular instances in a module.
    """
    # subclasses should have a component_class class variable

    def match(self, obj):
        return isinstance(obj, self.component_class)
   
    def register(self, context, name, instance, module_info, templates):
        raise NotImplementedError


class ModuleGrokker(GrokkerBase):
    """Grokker that gets executed once for a module.
    """

    def match(self, obj):
        # we never match with any object
        return False

    def register(self, context, module_info, templates):
        raise NotImplementedError


class Model(Contained, persistent.Persistent):
    # XXX Inheritance order is important here. If we reverse this,
    # then containers can't be models anymore because no unambigous MRO
    # can be established.
    pass


class Container(BTreeContainer):
    pass


class Site(SiteManagerContainer):
    pass


class Adapter(object):

    def __init__(self, context):
        self.context = context


class GlobalUtility(object):
    pass


class MultiAdapter(object):
    pass


class View(BrowserPage):
    interface.implements(interfaces.IGrokView)

    def __init__(self, context, request):
        super(View, self).__init__(context, request)
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

    def redirect(self, url):
        return self.request.response.redirect(url)

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
        resource.__name__ = self.__name
        return resource


class Traverser(object):
    interface.implements(IBrowserPublisher)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def browserDefault(self, request):
        view_name = getDefaultViewName(self.context, request)
        view_uri = "@@%s" % view_name
        return self.context, (view_uri,)

    def publishTraverse(self, request, name):
        subob = self.traverse(name)
        if subob:
            return subob

        # XXX special logic here to deal with views and containers.
        # would be preferrable if we could fall back on normal Zope
        # traversal behavior
        view = component.queryMultiAdapter((self.context, request), name=name)
        if view:
            return view

        if IReadContainer.providedBy(self.context):
            item = self.context.get(name)
            if item:
                return item

        raise NotFound(self.context, name, request)

    def traverse(self, name):
        # this will be overridden by subclasses
        pass


class ModelTraverser(Traverser):
    component.adapts(Model, IBrowserRequest)

    def traverse(self, name):
        traverse = getattr(self.context, 'traverse', None)
        if traverse:
            return traverse(name)


class ContainerTraverser(Traverser):
    component.adapts(Container, IBrowserRequest)

    def traverse(self, name):
        traverse = getattr(self.context, 'traverse', None)
        if traverse:
            result = traverse(name)
            if result is not None:
                return result
        # try to get the item from the container
        return self.context.get(name)


class Form(View):
    def __init__(self, context, request):
        super(Form, self).__init__(context, request)
        self.form = self.__real_form__(context, request)
        # we need this pointer to the actual grok-level form in our
        # custom Action
        self.form.grok_form = self

    def __call__(self):
        form = self.form

        form.update()

        # this code is extracted and modified from form.render

        # if the form has been updated, it may already have a result
        if form.form_result is None:
            # we reset, in case data has changed in a way that
            # causes the widgets to have different data
            if form.form_reset:
                form.resetForm()
                form.form_reset = False
            # recalculate result
            form.form_result = super(Form, self).__call__()

        return form.form_result


class EditForm(Form):
    label = ''
    status = ''

    def applyChanges(self, **data):
        if form.applyChanges(self.context, self.form.form_fields, data,
                             self.form.adapters):
            event.notify(ObjectModifiedEvent(self.context))
            self.status = "Updated"
        else:
            self.status = "No changes"


class AddForm(Form):
    label = ''
    status = ''


class DisplayForm(Form):
    label = ''
    status = ''
