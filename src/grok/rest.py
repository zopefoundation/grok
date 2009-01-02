"""Default REST view for Grok.

The views provided by this module get invoked when an object receives an
HTTP request in a REST skin for which no more-specific REST behavior has
been defined.  These all return the HTTP response Method Not Allowed.

"""
import grok
from grok.interfaces import IRESTSkinType

from zope import component
from zope.component.interfaces import ComponentLookupError
from zope.traversing.interfaces import TraversalError
from zope.traversing.namespace import view
from zope.interface import Interface
from zope.publisher.interfaces.http import IHTTPRequest
from zope.app.publication.http import MethodNotAllowed
from zope.publisher.browser import applySkin


class GrokMethodNotAllowed(MethodNotAllowed):
    """Exception indicating that an attempted REST method is not allowed."""


class MethodNotAllowedView(grok.MultiAdapter):
    """View rendering a REST GrokMethodNotAllowed exception over HTTP.

    Not only does this view render the REST error as an HTTP status of
    405 (Method Not Allowed) and a simple text message as the document
    body, but also offers an ``Allow:`` HTTP header listing any methods
    that can, in fact, succeed.  It constructs this list by testing the
    current object to see which methods it supports; if none of the
    standard methods succeed, then the ``Allow:`` header is still
    provided, but its value will be empty.

    """
    grok.adapts(GrokMethodNotAllowed, IHTTPRequest)
    grok.name('index.html')
    grok.implements(Interface)

    def __init__(self, error, request):
        self.error = error
        self.request = request
        self.allow = self._getAllow()

    def _getAllow(self):
        allow = []
        # List methods here in the same order that they should appear in
        # the "Allow:" header.
        for method in 'DELETE', 'GET', 'POST', 'PUT':
            view = component.queryMultiAdapter(
                (self.error.object, self.error.request),
                name=method)
            if view is not None:
                is_not_allowed = getattr(view, 'is_not_allowed', False)
                if not is_not_allowed:
                    allow.append(method)
        return allow

    def __call__(self):
        self.request.response.setHeader('Allow', ', '.join(self.allow))
        self.request.response.setStatus(405)
        return 'Method Not Allowed'


class rest_skin(view):
    """A rest skin.

    This used to be supported by zope.traversing but the change was
    backed out.  We need it for our REST support.

    """
    def traverse(self, name, ignored):
        self.request.shiftNameToApplication()
        try:
            skin = component.getUtility(IRESTSkinType, name)
        except ComponentLookupError:
            raise TraversalError("++rest++%s" % name)
        applySkin(self.request, skin)
        return self.context


class NotAllowedREST(grok.REST):
    """Default REST view, whose methods all raise Not Allowed errors.

    By binding itself to ``Interface``, this becomes the most general
    available REST view, and will be called into service for objects
    that have not had more specific REST views registered.  This means
    that such objects can at least return attractive refusals when
    clients attempt to assail them with unwanted HTTP methods.

    """
    grok.layer(grok.IRESTLayer)
    grok.context(Interface)

    is_not_allowed = True

    def GET(self):
        raise GrokMethodNotAllowed(self.context, self.request)

    def POST(self):
        raise GrokMethodNotAllowed(self.context, self.request)

    def PUT(self):
        raise GrokMethodNotAllowed(self.context, self.request)

    def DELETE(self):
        raise GrokMethodNotAllowed(self.context, self.request)
