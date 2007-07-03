import zope.component
import zope.interface
from zope.component.interfaces import ComponentLookupError
from zope.publisher.browser import BrowserPage
from zope.publisher.publish import mapply
from zope.pagetemplate.interfaces import IPageTemplate

from z3c.template.interfaces import ILayoutTemplate

import grok
from grok.interfaces import IGrokView

class ViewBase(object):

    template_name = u''

    def application(self):
        obj = self.context
        while obj is not None:
            if isinstance(obj, grok.Application):
                return obj
            obj = obj.__parent__
        raise ValueErrror("No application found.")

    def site(self):
        obj = self.context
        while obj is not None:
            if isinstance(obj, grok.Site):
                return obj
            obj = obj.__parent__
        raise ValueErrror("No site found.")

    def application_url(self, name=None):
        obj = self.context
        while obj is not None:
            if isinstance(obj, grok.Application):
                return self.url(obj, name)
            obj = obj.__parent__
        raise ValueErrror("No application found.")

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
        return url(self.request, obj, name)
        
    def redirect(self, url):
        return self.request.response.redirect(url)
        
    @property
    def response(self):
        return self.request.response

    def update(self):
        pass

    def __getitem__(self, key):
        # XXX give nice error message if template is None
        return self.template.macros[key]


class View(BrowserPage, ViewBase):
    """Chief difference here between grok.View is that this is registered not on
    IDefaultBrowserLayer but on IBrowserRequest so that it is available to MinimalLayer
    which does not subclass IDefaultBrowserLayer"""
    zope.interface.implements(IGrokView)

    def __init__(self, context, request):
        super(View, self).__init__(context, request)
        self.static = zope.component.queryAdapter(
            self.request,
            zope.interface.Interface,
            name=self.module_info.package_dotted_name
            )

    def __call__(self):
        """note that I've lost the static directory in the namespace,
        to bring this back in would mean changes to z3c.template.

        I'll think again about this further on"""
        # should check if update() is not called elsewhere
        mapply(self.update, (), self.request)
        if self.request.response.getStatus() in (302, 303):
            return
        template = getattr(self, 'template', None)
        if template is None:
            try:
                template = zope.component.getMultiAdapter(
                    (self, self.request), IPageTemplate)
                return template(self)
            except ComponentLookupError:
                pass
        else:
            return template(self)
        return mapply(self.render, (), self.request)


class ITemplateView(zope.interface.Interface):
    pass

class TemplateView(BrowserPage, ViewBase):
    """This differs from the above in that instead of expecting a template
    or render method, the template will be looked up.
    No call method is provided.
    
    This is at the moment experimentation with z3c.template package.

    Probable it will go away and I'll just use megrok.pagelet.
    """
    zope.interface.implements(ITemplateView)
    template = None

    def __init__(self, context, request):
        super(TemplateView, self).__init__(context, request)
        self.static = zope.component.queryAdapter(
            self.request,
            zope.interface.Interface,
            name=self.module_info.package_dotted_name
            )

    def render(self):
        mapply(self.update, (), self.request)
        if self.request.response.getStatus() in (302, 303):
            return
        template = getattr(self, 'template', None)
        if template is None:
            template = zope.component.getMultiAdapter(
                (self, self.request), IPageTemplate)
            return template(self)
        return template(self)

class ILayoutView(zope.interface.Interface):
    pass

class LayoutView(BrowserPage, ViewBase):
    """This differs from the above in that instead of expecting a template
    or render method, a layout template will be looked up in the call method
    
    This is at the moment experimentation with z3c.template package.

    Probable it will go away and I'll just use megrok.pagelet.
    """
    zope.interface.implements(ILayoutView)
    layout = None

    def __init__(self, context, request):
        super(LayoutView, self).__init__(context, request)
        self.static = zope.component.queryAdapter(
            self.request,
            zope.interface.Interface,
            name=self.module_info.package_dotted_name
            )

    def __call__(self):
        mapply(self.update, (), self.request)
        if self.request.response.getStatus() in (302, 303):
            return
        layout = getattr(self, 'layout', None)
        if layout is None:
            layout = zope.component.getMultiAdapter(
                (self, self.request), ILayoutTemplate)
            return layout(self)
        return layout(self)

    def render(self):
        pass
