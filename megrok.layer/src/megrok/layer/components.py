from zope.publisher.interfaces.browser import IBrowserRequest
import zope.interface
from z3c.layer.pagelet import IPageletBrowserLayer
from z3c.layer.minimal import IMinimalBrowserLayer

class ILayer(zope.interface.Interface):
    pass

class IMinimalLayer(ILayer, IMinimalBrowserLayer):
    pass

class IPageletLayer(ILayer, IPageletBrowserLayer):
    pass

class Skin(object):
    pass

