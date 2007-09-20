import grok

from zope import component

from zope.traversing.namespace import skin
from zope.interface import Interface
from zope.interface.interfaces import IInterface
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.publisher.interfaces.http import IHTTPRequest

from grok.components import GrokMethodNotAllowed

class IRESTSkinType(IInterface):
    """Skin for REST requests.
    """

class MethodNotAllowedView(grok.MultiAdapter):
    grok.adapts(GrokMethodNotAllowed, IHTTPRequest)
    grok.name('index.html')
    grok.implements(Interface)
    
    def __init__(self, error, request):
        self.error = error
        self.request = request
        self.allow = self._getAllow()
        
    def _getAllow(self):
        allow = []
        for method in ['GET', 'PUT', 'POST', 'DELETE']:
            view = component.queryMultiAdapter(
                (self.error.object, self.error.request),
                name=method)
            if view is not None and not view.is_not_allowed:
                allow.append(method)
        allow.sort()
        return allow
    
    def __call__(self):
        self.request.response.setHeader('Allow', ', '.join(self.allow))
        self.request.response.setStatus(405)
        return 'Method Not Allowed'
    
class rest_skin(skin):
    skin_type = IRESTSkinType

class DefaultRest(grok.REST):
    grok.context(Interface)
    grok.layer(grok.IRESTLayer)
