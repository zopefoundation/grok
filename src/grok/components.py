##############################################################################
#
# Copyright (c) 2006-2007 Zope Foundation and Contributors.
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
"""Base classes for Grok application components.

When an application developer builds a Grok-based application, the
classes they define each typically inherit from one of the base classes
provided here.

"""
import os.path
import zope.location
import zope.errorview.browser
import zope.component
from zope.container.interfaces import IReadContainer
from zope import component
from zope import interface
from zope.interface.common.interfaces import IException
from zope.publisher.browser import BrowserPage
from zope.publisher.defaultview import getDefaultViewName
from zope.publisher.interfaces.browser import IBrowserPublisher
from zope.publisher.interfaces.http import IHTTPRequest
from zope.publisher.interfaces import INotFound
from zope.publisher.interfaces import NotFound
from zope.publisher.publish import mapply
from zope.security.interfaces import IUnauthorized

import grok
import martian.util

import grokcore.view
import grokcore.site
import grokcore.message
import grokcore.layout
import grokcore.layout.components
from grok import interfaces, util

# BBB this is for import backward compatibility.
from grokcore.xmlrpc import XMLRPC
from grokcore.rest import REST
from grokcore.json import JSON
from grokcore.content import Container
from grokcore.content import Model
from grokcore.content import OrderedContainer
from grokcore.site import Application
from grokcore.view.util import ASIS


class ViewSupportMixin(object):

    def application_url(self, name=None, skin=ASIS, data=None):
        """Return the URL of the closest :class:`grok.Application` object in
        the hierarchy or the URL of a named object (``name``
        parameter) relative to the closest application object.
        """
        return util.application_url(
            self.request, self.context, name=name, skin=skin, data=data)

    def flash(self, message, type='message'):
        """Send a short message to the user."""
        grokcore.message.send(message, type=type, name='session')


@interface.implementer(interfaces.IGrokView)
class View(ViewSupportMixin, grokcore.view.View):
    """The base class for views with templates in Grok applications.

    Implements the :class:`grokcore.view.interfaces.IGrokView`
    interface.

    Each class that inherits from `grok.View` is designed to "render" a
    category of content objects by reducing them to a document (often an
    HTML document).  Every view has a name, and is invoked when users
    visit the URL of an eligible context object followed by the name of
    the view itself::

        http://example.com/app/folder/object/viewname

    If the view name might conflict with actual content inside of the
    context (in the above URL, the context might already contain an
    attribute or item named ``viewname``), then the URL can be explicit
    that it is asking for a view by preceding its name with ``@@``::

        http://example.com/app/folder/object/@@viewname

    Instead of returning a full document, views are sometimes used to
    provide only a snippet of information for inclusion in some larger
    document; the view can then be called from inside of another view's
    page template::

        <li tal:content="context/@@viewname">snippet goes here</li>

    A view class can specify the category of objects that it can render
    by calling the `grok.context()` directive with either a class or an
    interface.  Otherwise, Grok will attempt to determine the context
    automatically by searching the view's module for exactly one
    `grok.Model` or `grok.Container` class (or some other class
    providing the interface `IContext`) and using that class, if found.

    Grok normally creates a view's name (the name used in URLs) by
    downcasing the name of the view class itself.  The developer can
    override this by supplying the `grok.name()` directive instead.

    The view name ``index`` is special (this works whether the view
    class itself is named ``Index``, or whether ``grok.name('index')``
    is used instead).  A view named ``index`` is used to render an
    object when the user visits its URL without appending a view name.

    Each view needs to generate and return a document. There are two
    ways of doing so: either the view can provide a `render()` method
    that returns a document, or the view can be associated with a page
    template that Grok will.  Page templates can be associated with a
    view in three different ways:

    * Grok will automatically associate a view with a page template
      defined in an accompanying ``templates`` directory.  If a view
      class ``MammothList`` occurs in a module ``<src>/animal.py``, for
      example, then Grok will look for a page template with the name
      ``<src>/animal_templates/mammothlist.pt``, where ``.pt`` can be
      any page-template extension recognized by Grok.

    * Grok will automatically associate a view with a page template
      object in the same module whose name is the downcased name of the
      view class itself.  For example, a view ``MammothList`` might be
      defined in a module alongside an actual template instance named
      ``mammothlist``.

    * The developer can explicitly define the path to the page template
      file by providing the ``grok.template()`` directive.

    Before a page template is rendered, Grok will call the `update()`
    method on the view, if one is supplied, which can pre-compute values
    that the template will need to display.  Both `render()` methods and
    `update()` methods will find the context for which the view is being
    rendered under ``self.context``.

    """
    grok.baseclass()

    def application_url(self, name=None, skin=ASIS, data=None):
        """Return the URL of the closest :class:`grok.Application` object in
        the hierarchy or the URL of a named object (``name``
        parameter) relative to the closest application object.
        """
        return util.application_url(
            self.request, self.context, name=name, skin=skin, data=data)

    def flash(self, message, type='message'):
        """Send a short message to the user."""
        grokcore.message.send(message, type=type, name='session')


class ExceptionView(View, zope.errorview.browser.ExceptionView):
    """Base class for rendering views for uncaught exceptions that occur during
    the application run-time and are not otherwise rendered.

    Note that when this class in not subclassed, the default error view from
    zope.errorview is being rendered.
    """
    grok.baseclass()
    grok.context(IException)
    grok.name('index')

    def update(self):
        return zope.errorview.browser.ExceptionView.update(self)

    def render(self):
        """An error view can either be rendered by an associated template, or
        it can implement this method to render itself from Python. This is
        useful if the view's output isn't XML/HTML but something computed in
        Python (plain text, PDF, etc.)

        Contrary to regular views, render() does *not* accept any parameters.
        """
        return zope.errorview.browser.ExceptionView.render(self)

    render.base_method = True


class NotFoundView(View, zope.errorview.browser.NotFoundView):
    """Base class for rendering views for INotFound exceptions.

    Note that when this class in not subclassed, the default error view from
    zope.errorview is being rendered.
    """
    grok.baseclass()
    grok.context(INotFound)
    grok.name('index')

    def update(self):
        return zope.errorview.browser.NotFoundView.update(self)

    def render(self):
        """An error view can either be rendered by an associated template, or
        it can implement this method to render itself from Python. This is
        useful if the view's output isn't XML/HTML but something computed in
        Python (plain text, PDF, etc.)

        Contrary to regular views, render() does *not* accept any parameters.
        """
        return zope.errorview.browser.NotFoundView.render(self)

    render.base_method = True


class UnauthorizedView(View, zope.errorview.browser.UnauthorizedView):
    """Base class for rendering views for IUnauthorized exceptions.

    Note that when this class in not subclassed, the default error view from
    zope.errorview is being rendered.
    """
    grok.baseclass()
    grok.context(IUnauthorized)
    grok.name('index')

    def update(self):
        return zope.errorview.browser.UnauthorizedView.update(self)

    def render(self):
        """An error view can either be rendered by an associated template, or
        it can implement this method to render itself from Python. This is
        useful if the view's output isn't XML/HTML but something computed in
        Python (plain text, PDF, etc.)

        Contrary to regular views, render() does *not* accept any parameters.
        """
        return zope.errorview.browser.UnauthorizedView.render(self)

    render.base_method = True


@interface.implementer(interfaces.IGrokForm)
class Form(ViewSupportMixin, grokcore.formlib.Form):
    """The base class for forms in Grok applications.

    A class that inherits from :class:`grok.Form` is a
    :class:`grok.View` whose template will be given information about
    the fields in its context, and use that information to render an
    HTML form for adding or editing the form.  Generally developers
    use one of the subclasses:

    * :class:`grok.AddForm`
    * :class:`grok.DisplayForm`
    * :class:`grok.EditForm`

    """
    grok.baseclass()


@interface.implementer(interfaces.IGrokForm)
class AddForm(ViewSupportMixin, grokcore.formlib.AddForm):
    """Base class for add forms in Grok applications."""
    grok.baseclass()


@interface.implementer(interfaces.IGrokForm)
class DisplayForm(ViewSupportMixin, grokcore.formlib.DisplayForm):
    """Base class for display forms in Grok applications."""
    grok.baseclass()


@interface.implementer(interfaces.IGrokForm)
class EditForm(ViewSupportMixin, grokcore.formlib.EditForm):
    """Base class for edit forms in Grok applications."""
    grok.baseclass()


class Layout(ViewSupportMixin, grokcore.layout.Layout):
    grok.baseclass()

class Page(ViewSupportMixin, grokcore.layout.Page):
    grok.baseclass()

# Default forms for form without the html and body tags
default_form_template = grokcore.view.PageTemplateFile(
    os.path.join('templates', 'default_edit_form.pt'))

default_form_template.__grok_name__ = 'default_edit_form'

default_display_template = grokcore.view.PageTemplateFile(
    os.path.join('templates', 'default_display_form.pt'))

default_display_template.__grok_name__ = 'default_display_form'

class LayoutAwareFormPage(grokcore.layout.components.LayoutAware):
    """A mixin to make form aware of layouts.
    """
    def __call__(self):
        """Calls update and returns the layout template which calls render.
        """
        self.layout = self._get_layout()
        mapply(self.update, (), self.request)
        if self.request.response.getStatus() in (302, 303):
            # A redirect was triggered somewhere in update().  Don't
            # continue rendering the template or doing anything else.
            return
        # update_form() is what make a layout-aware form different from
        # 'regular" layout-aware component.
        self.update_form()
        if self.request.response.getStatus() in (302, 303):
            return
        return self.layout(self)


class FormPage(
    ViewSupportMixin,
    LayoutAwareFormPage,
    grokcore.formlib.Form
    ):
    """A form base class.
    """
    grok.baseclass()
    template = default_form_template


class AddFormPage(
    ViewSupportMixin,
    LayoutAwareFormPage,
    grokcore.formlib.AddForm
    ):
    """Base add form.
    """
    grok.baseclass()
    template = default_form_template


class EditFormPage(
    ViewSupportMixin,
    LayoutAwareFormPage,
    grokcore.formlib.EditForm
    ):
    """Base edit form.
    """
    grok.baseclass()
    template = default_form_template


class DisplayFormPage(
    ViewSupportMixin,
    LayoutAwareFormPage,
    grokcore.formlib.DisplayForm
    ):
    """Base display form.
    """
    grok.baseclass()
    template = default_display_template
