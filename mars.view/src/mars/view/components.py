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
    """Maybe this could be in the grok.components module?
    
    All of this is directly copied from grok.View"""

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
        # give nice error message if template is None
        return self.template.macros[key]

class TemplateViewBase(ViewBase):
    """Mixin to reuse render method"""
    template = None
    _template_name = u'' # will be set if grok.template defined
    _template_interface = IPageTemplate

    def render(self):
        mapply(self.update, (), self.request)
        if self.request.response.getStatus() in (302, 303):
            return
        template = getattr(self, 'template', None)
        if template is None:
            template = zope.component.getMultiAdapter(
                (self, self.request), self._template_interface, 
                name=self._template_name)
            return template(self)
        return template(self)


class TemplateView(TemplateViewBase, BrowserPage):

    def __init__(self, context, request):
        super(TemplateView, self).__init__(context, request)


class LayoutView(TemplateViewBase, BrowserPage):
    layout = None
    _layout_name = u'' # will be set if mars.view.layout defined
    _layout_interface = ILayoutTemplate

    def __init__(self, context, request):
        super(LayoutView, self).__init__(context, request)

    def __call__(self):
        mapply(self.update, (), self.request)
        if self.request.response.getStatus() in (302, 303):
            return
        layout = getattr(self, 'layout', None)
        if layout is None:
            layout = zope.component.getMultiAdapter(
                    (self, self.request), self._layout_interface, 
                    name=self._layout_name)
            return layout(self)
        return layout(self)

