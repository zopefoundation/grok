import zope.component
import zope.interface
from zope.publisher.browser import BrowserPage
from zope.publisher.publish import mapply
from zope.pagetemplate.interfaces import IPageTemplate

from z3c.template.interfaces import ILayoutTemplate

import grok
from grok.interfaces import IGrokView

class ViewBase(object):

    def _render_template(self):
        namespace = self.template.pt_getContext()
        namespace['request'] = self.request
        namespace['view'] = self
        namespace['context'] = self.context
        namespace['static'] = self.static
        return self.template.pt_render(namespace)

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
    zope.interface.implements(IGrokView)

    def __init__(self, context, request):
        super(View, self).__init__(context, request)
        self.static = zope.component.queryAdapter(
            self.request,
            zope.interface.Interface,
            name=self.module_info.package_dotted_name
            )

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

    def _render_template(self):
        # z3c.template factory is a z.a.viewpagetemplatefile
        namespace = self.template.pt_getContext(self, self.request)
        namespace['request'] = self.request
        namespace['view'] = self
        namespace['context'] = self.context
        namespace['static'] = self.static
        #for key in namespace.keys():
        #    print key
        return self.template.pt_render(namespace)

    def render(self):
        # should check if update() is not called elsewhere
        mapply(self.update, (), self.request)
        if self.template is None:
            self.template = zope.component.getMultiAdapter(
                (self, self.request), IPageTemplate)
            self.template.macro = None
            return self._render_template()
        return self._render_template()

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

    def _render_layout(self):
        # z3c.template factory is a z.a.viewpagetemplatefile
        namespace = self.layout.pt_getContext(self, self.request)
        namespace['request'] = self.request
        namespace['view'] = self
        namespace['context'] = self.context
        namespace['static'] = self.static
        return self.layout.pt_render(namespace)

    def __call__(self):
        # should check if update() is not called elsewhere
        mapply(self.update, (), self.request)
        if self.layout is None:
            self.layout = zope.component.getMultiAdapter(
                (self, self.request), ILayoutTemplate)
            return self._render_layout()
        return self._render_layout()

