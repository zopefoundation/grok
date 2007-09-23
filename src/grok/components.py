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
"""Grok components"""

import os
import persistent
import urllib
import datetime
import warnings
import pytz
import simplejson

from zope import component
from zope import interface
from zope.interface.common import idatetime
from zope.security.permission import Permission
from zope.app.securitypolicy.role import Role
from zope.publisher.browser import BrowserPage
from zope.publisher.interfaces import NotFound
from zope.publisher.interfaces.browser import (IBrowserPublisher,
                                               IBrowserRequest)
from zope.publisher.publish import mapply
from zope.pagetemplate import pagetemplate, pagetemplatefile
from zope.formlib import form
from zope.annotation.interfaces import IAttributeAnnotatable

from zope.app.pagetemplate.engine import TrustedAppPT
from zope.app.publisher.browser import getDefaultViewName
from zope.app.publisher.browser import directoryresource
from zope.app.publisher.browser.pagetemplateresource import \
    PageTemplateResourceFactory
from zope.app.container.btree import BTreeContainer
from zope.app.container.contained import Contained
from zope.app.container.interfaces import IReadContainer
from zope.app.component.site import SiteManagerContainer

import z3c.flashmessage.interfaces

import martian.util
from grok import interfaces, formlib, util


class Model(Contained, persistent.Persistent):
    # XXX Inheritance order is important here. If we reverse this,
    # then containers can't be models anymore because no unambigous MRO
    # can be established.
    interface.implements(IAttributeAnnotatable)


class Container(BTreeContainer):
    interface.implements(IAttributeAnnotatable)


class Site(SiteManagerContainer):
    pass


class Application(Site):
    """A top-level application object."""
    interface.implements(interfaces.IApplication)


class Adapter(object):

    def __init__(self, context):
        self.context = context


class GlobalUtility(object):
    pass


class LocalUtility(Model):
    pass


class MultiAdapter(object):
    pass


class Annotation(persistent.Persistent):
    pass


class View(BrowserPage):
    interface.implements(interfaces.IGrokView)

    def __init__(self, context, request):
        super(View, self).__init__(context, request)
        self.__name__ = self.__view_name__
        self.static = component.queryAdapter(
            self.request,
            interface.Interface,
            name=self.module_info.package_dotted_name
            )

    @property
    def response(self):
        return self.request.response

    def __call__(self):
        mapply(self.update, (), self.request)
        if self.request.response.getStatus() in (302, 303):
            # A redirect was triggered somewhere in update().  Don't
            # continue rendering the template or doing anything else.
            return

        template = getattr(self, 'template', None)
        if template is not None:
            return self._render_template()
        return mapply(self.render, (), self.request)

    def _render_template(self):
        namespace = self.template.pt_getContext()
        namespace['request'] = self.request
        namespace['view'] = self
        namespace['context'] = self.context
        # XXX need to check whether we really want to put None here if missing
        namespace['static'] = self.static
        return self.template.pt_render(namespace)

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
        return util.url(self.request, obj, name)

    def application_url(self, name=None):
        obj = self.context
        while obj is not None:
            if isinstance(obj, Application):
                return self.url(obj, name)
            obj = obj.__parent__
        raise ValueError("No application found.")

    def redirect(self, url):
        return self.request.response.redirect(url)

    def update(self):
        pass

    def flash(self, message, type='message'):
        source = component.getUtility(
            z3c.flashmessage.interfaces.IMessageSource, name='session')
        source.send(message, type)


class XMLRPC(object):
    pass


class JSON(BrowserPage):

    def __call__(self):
        view_name = self.__view_name__
        method = getattr(self, view_name)
        method_result = mapply(method, (), self.request)
        return simplejson.dumps(method_result)


class GrokPageTemplate(object):

    def __repr__(self):
        return '<%s template in %s>' % (self.__grok_name__,
                                        self.__grok_location__)

    def _annotateGrokInfo(self, name, location):
        self.__grok_name__ = name
        self.__grok_location__ = location


class PageTemplate(GrokPageTemplate, TrustedAppPT, pagetemplate.PageTemplate):
    expand = 0

    def __init__(self, template):
        super(PageTemplate, self).__init__()
        if martian.util.not_unicode_or_ascii(template):
            raise ValueError("Invalid page template. Page templates must be "
                             "unicode or ASCII.")
        self.write(template)

        # __grok_module__ is needed to make defined_locally() return True for
        # inline templates
        # XXX unfortunately using caller_module means that
        # PageTemplate cannot be subclassed
        self.__grok_module__ = martian.util.caller_module()


class PageTemplateFile(GrokPageTemplate, TrustedAppPT,
                       pagetemplatefile.PageTemplateFile):

    def __init__(self, filename, _prefix=None):
        _prefix = self.get_path_from_prefix(_prefix)
        super(PageTemplateFile, self).__init__(filename, _prefix)

        # __grok_module__ is needed to make defined_locally() return True for
        # inline templates
        # XXX unfortunately using caller_module means that
        # PageTemplateFile cannot be subclassed
        self.__grok_module__ = martian.util.caller_module()


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
        if subob is not None:
            return util.safely_locate_maybe(subob, self.context, name)

        # XXX Special logic here to deal with containers.  It would be
        # good if we wouldn't have to do this here. One solution is to
        # rip this out and make you subclass ContainerTraverser if you
        # wanted to override the traversal behaviour of containers.
        if IReadContainer.providedBy(self.context):
            item = self.context.get(name)
            if item is not None:
                return item

        view = component.queryMultiAdapter((self.context, request), name=name)
        if view is not None:
            return view

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


default_form_template = PageTemplateFile(os.path.join(
    'templates', 'default_edit_form.pt'))
default_form_template.__grok_name__ = 'default_edit_form'
default_display_template = PageTemplateFile(os.path.join(
    'templates', 'default_display_form.pt'))
default_display_template.__grok_name__ = 'default_display_form'


class GrokForm(object):
    """Mix-in to console zope.formlib's forms with grok.View and to
    add some more useful methods.

    The consolation needs to happen because zope.formlib's Forms have
    update/render methods which have different meanings than
    grok.View's update/render methods.  We deal with this issue by
    'renaming' zope.formlib's update() to update_form() and by
    disallowing subclasses to have custom render() methods."""

    def update(self):
        """Subclasses can override this method just like on regular
        grok.Views. It will be called before any form processing
        happens."""

    def update_form(self):
        """Update the form, i.e. process form input using widgets.

        On zope.formlib forms, this is what the update() method is.
        In grok views, the update() method has a different meaning.
        That's why this method is called update_form() in grok forms."""
        super(GrokForm, self).update()

    def render(self):
        """Render the form, either using the form template or whatever
        the actions returned in form_result."""
        # if the form has been updated, it will already have a result
        if self.form_result is None:
            if self.form_reset:
                # we reset, in case data has changed in a way that
                # causes the widgets to have different data
                self.resetForm()
                self.form_reset = False
            self.form_result = self._render_template()

        return self.form_result

    # Mark the render() method as a method from the base class. That
    # way we can detect whether somebody overrides render() in a
    # subclass (which we don't allow).
    render.base_method = True

    def __call__(self):
        mapply(self.update, (), self.request)
        if self.request.response.getStatus() in (302, 303):
            # A redirect was triggered somewhere in update().  Don't
            # continue rendering the template or doing anything else.
            return

        self.update_form()
        return self.render()


class Form(GrokForm, form.FormBase, View):
    # We're only reusing the form implementation from zope.formlib, we
    # explicitly don't want to inherit the interface semantics (mostly
    # for the different meanings of update/render).
    interface.implementsOnly(interfaces.IGrokForm)

    template = default_form_template

    def applyData(self, obj, **data):
        return formlib.apply_data_event(obj, self.form_fields, data,
                                        self.adapters)

    # BBB -- to be removed in June 2007
    def applyChanges(self, obj, **data):
        warnings.warn("The 'applyChanges' method on forms is deprecated "
                      "and will disappear by June 2007. Please use "
                      "'applyData' instead.", DeprecationWarning, 2)
        return bool(self.applyData(obj, **data))


class AddForm(Form):
    pass


class EditForm(GrokForm, form.EditFormBase, View):
    # We're only reusing the form implementation from zope.formlib, we
    # explicitly don't want to inherit the interface semantics (mostly
    # for the different meanings of update/render).
    interface.implementsOnly(interfaces.IGrokForm)

    template = default_form_template

    def applyData(self, obj, **data):
        return formlib.apply_data_event(obj, self.form_fields, data,
                                        self.adapters, update=True)

    # BBB -- to be removed in June 2007
    def applyChanges(self, obj, **data):
        warnings.warn("The 'applyChanges' method on forms is deprecated "
                      "and will disappear by June 2007. Please use "
                      "'applyData' instead.", DeprecationWarning, 2)
        return bool(self.applyData(obj, **data))

    @formlib.action("Apply")
    def handle_edit_action(self, **data):
        if self.applyData(self.context, **data):
            formatter = self.request.locale.dates.getFormatter(
                'dateTime', 'medium')

            try:
                time_zone = idatetime.ITZInfo(self.request)
            except TypeError:
                time_zone = pytz.UTC

            self.status = "Updated on %s" % formatter.format(
                datetime.datetime.now(time_zone)
                )
        else:
            self.status = 'No changes'


class DisplayForm(GrokForm, form.DisplayFormBase, View):
    # We're only reusing the form implementation from zope.formlib, we
    # explicitly don't want to inherit the interface semantics (mostly
    # for the different meanings of update/render).
    interface.implementsOnly(interfaces.IGrokForm)

    template = default_display_template


class IndexesClass(object):
    def __init__(self, name, bases=(), attrs=None):
        if attrs is None:
            return
        # make sure we take over a bunch of possible attributes
        for name in ['__grok_context__', '__grok_name__',
                     '__grok_site__']:
            value = attrs.get(name)
            if value is not None:
                setattr(self, name, value)
        # now read and store indexes
        indexes = {}
        for name, value in attrs.items():
            if not interfaces.IIndexDefinition.providedBy(value):
                continue
            indexes[name] = value
        self.__grok_indexes__ = indexes
        # __grok_module__ is needed to make defined_locally() return True for
        # inline templates
        self.__grok_module__ = martian.util.caller_module()

Indexes = IndexesClass('Indexes')

class Permission(Permission):
    pass

class Role(Role):
    pass

class IGrokLayer(interface.Interface):
    pass

class Skin(object):
    pass
