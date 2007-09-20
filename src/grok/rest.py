import grok

from zope.traversing.namespace import skin
from zope.interface import Interface
from zope.interface.interfaces import IInterface
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.publisher.interfaces.http import IHTTPRequest
from zope.app.publication.http import MethodNotAllowed

class IRESTSkinType(IInterface):
    """Skin for REST requests.
    """
    
class rest_skin(skin):
    skin_type = IRESTSkinType

class DefaultRest(grok.REST):
    grok.context(Interface)
    grok.layer(grok.IRESTLayer)
    
